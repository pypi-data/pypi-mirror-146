"""Image Parcel Aggregation with Clustering (impac)."""

# Authors: Pierre Bellec
# License: BSD 3 clause
import warnings

from scipy.sparse import vstack
import numpy as np

from sklearn.utils import check_random_state
from sklearn.preprocessing import StandardScaler
import dypac.bascpp as bpp
from dypac.embeddings import Embedding


def _sanitize_imgs(imgs):
    """Check that provided images are in the correct format."""
    if type(imgs) is not np.ndarray:
        raise ValueError("imgs should be a numpy array.")

    if len(imgs.shape) < 3:
        raise ValueError("imgs size should be n_samp * n_x * n_y * n_channels")

    return imgs


class Impac:
    """
    Perform Stable Dynamic Cluster Analysis on images.

    Parameters
    ----------
    n_clusters: int, optional
        Number of clusters to extract per time window

    n_states: int, optional
        Number of expected dynamic states

    n_replications: int, optional
        Number of replications of cluster analysis in each fMRI run

    n_batch: int, optional
        Number of batches to run through consensus clustering.
        If n_batch<=1, consensus clustering will be applied
        to all replications in one pass. Processing with batch will
        reduce dramatically the compute time, but will change slightly
        the results.

    n_init: int, optional
        Number of initializations for k-means

    subsample_size: int, optional
        Number of time points in a subsample

    max_iter: int, optional
        Max number of iterations for k-means

    threshold_sim: float (0 <= . <= 1), optional
        Minimal acceptable average dice in a state

    random_state: int or RandomState, optional
        Pseudo number generator state used for random sampling.

    standardize: boolean, optional
        If standardize is True, the values of each image are centered and normed:
        their mean is put to 0 and their variance to 1 across examples

    verbose: integer, optional
        Indicate the level of verbosity. By default, print progress.

    """

    def __init__(
        self,
        n_clusters=10,
        n_states=3,
        n_replications=40,
        n_batch=1,
        n_init=30,
        n_init_aggregation=100,
        subsample_size=1,
        max_iter=30,
        threshold_sim=0.3,
        random_state=None,
        standardize=True,
        verbose=1,
    ):
        """Set up default attributes for the class."""
        self.n_clusters = n_clusters
        self.n_states = n_states
        self.n_batch = n_batch
        self.n_replications = n_replications
        self.n_init = n_init
        self.n_init_aggregation = n_init_aggregation
        self.subsample_size = subsample_size
        self.max_iter = max_iter
        self.threshold_sim = threshold_sim
        self.random_state = random_state
        self.standardize = standardize
        self.verbose = verbose

    def _check_components_(self):
        """Check for presence of estimated components."""
        if not hasattr(self, "components_"):
            raise ValueError(
                "Object has no components_ attribute. "
                "This is probably because fit has not "
                "been called."
            )

    def _check_n_batch_(self, imgs):
        # Check that number of batches is reasonable
        if self.n_batch > imgs.shape[0]:
            warnings.warn(
                "{0} batches were requested, but only {1} datasets available. Using {2} batches instead.".format(
                    self.n_batch, imgs.shape[0], imgs.shape[0]
                )
            )
            self.n_batch = imgs.shape[0]

    def fit(self, imgs, confounds=None):
        """
        Compute the parcels across images.

        Parameters
        ----------
        imgs: ndarray with a series of images.
            imgs size should be n_samp * n_x * n_y * n_channels

        Returns
        -------
        self: object
            Returns the instance itself. Contains attributes listed
            at the object level.
        """
        imgs = _sanitize_imgs(imgs)
        self.imgs_shape_ = imgs.shape

        # Control random number generation
        self.random_state = check_random_state(self.random_state)
        self._check_n_batch_(imgs)

        # mask_and_reduce step
        if self.n_batch > 1:
            stab_maps, dwell_time = self._mask_and_reduce_batch(imgs)
        else:
            stab_maps, dwell_time = self._mask_and_reduce(imgs)

        # Return components
        self.components_ = stab_maps
        self.dwell_time_ = dwell_time

        # Create embedding
        self.embedding = Embedding(stab_maps.todense())
        return self

    def _mask_and_reduce_batch(self, imgs, confounds=None):
        """Iterate impac on batches of files."""
        stab_maps_list = []
        dwell_time_list = []
        for bb in range(self.n_batch):
            slice_batch = slice(bb, imgs.shape[0], self.n_batch)
            if self.verbose:
                print("[{0}] Processing batch {1}".format(self.__class__.__name__, bb))
            stab_maps, dwell_time = self._mask_and_reduce(imgs[slice_batch])
            stab_maps_list.append(stab_maps)
            dwell_time_list.append(dwell_time)

        stab_maps_cons, dwell_time_cons = bpp.consensus_batch(
            stab_maps_list,
            dwell_time_list,
            self.n_replications,
            self.n_states,
            self.max_iter,
            self.n_init_aggregation,
            self.random_state,
            self.verbose,
        )

        return stab_maps_cons, dwell_time_cons

    def _mask_and_reduce(self, imgs, confounds=None):
        """
        Cluster aggregation on a list of images.

        Returns
        -------
        stab_maps: ndarray
            stability maps of each state.

        dwell_time: ndarray
            dwell time of each state.
        """
        onehot_list = []
        this_data = self._load_imgs(imgs, standardize=self.standardize)
        onehot = bpp.replicate_clusters(
            this_data,
            subsample_size=self.subsample_size,
            n_clusters=self.n_clusters,
            n_replications=self.n_replications,
            max_iter=self.max_iter,
            n_init=self.n_init,
            random_state=self.random_state,
            verbose=self.verbose,
        )

        # find the states
        states = bpp.find_states(
            onehot,
            n_states=self.n_states,
            max_iter=self.max_iter,
            threshold_sim=self.threshold_sim,
            random_state=self.random_state,
            n_init=self.n_init_aggregation,
            verbose=self.verbose,
        )

        # Generate the stability maps
        stab_maps, dwell_time = bpp.stab_maps(
            onehot, states, self.n_replications, self.n_states
        )

        return stab_maps, dwell_time

    def _load_imgs(self, img, standardize):
        """
        Load a series of images in the right format for impac.
        """
        if len(img.shape) == 3:
            [n_samp, nx, ny] = img.shape
            img = img.reshape([n_samp, nx * ny])
        else:
            [n_samp, nx, ny, nc] = img.shape
            img = img.reshape([n_samp, nx * ny * nc])
        if standardize:
            img_r = StandardScaler().fit_transform(img.transpose())
        else:
            img_r = img.transpose()
        return img_r

    def _array2imgs(self, tseries):
        """
        Reshape an array of images into proper shape.
        """
        if len(self.imgs_shape_) == 3:
            imgs = np.reshape(tseries,
                [tseries.shape[0], self.imgs_shape_[1], self.imgs_shape_[2]]
            )
        else:
            imgs = np.reshape(tseries,
                [
                    tseries.shape[0],
                    self.imgs_shape_[1],
                    self.imgs_shape_[2],
                    self.imgs_shape_[3],
                ]
            )
        return imgs

    def _check_size_img(self, imgs):
        if not np.array_equal(imgs.shape[1:], self.imgs_shape_[1:]):
            raise ValueError("provided images do not match the size of training data.")

    def transform(self, imgs):
        """
        Transform an image in embedding coefficients.

        Parameters
        ----------
        imgs: ndarray with a series of images.
            imgs size should be n_samp * n_x * n_y * n_channels

        Returns
        -------
        weights : numpy array of shape [n_samp, n_states + 1]
            The image after projection in the parcellation space.
            Note that the first coefficient corresponds to the intercept,
            and not one of the parcels.
        """
        self._check_components_()
        self._check_size_img(imgs)
        tseries = self._load_imgs(imgs, standardize=False).transpose()
        return self.embedding.transform(tseries)

    def inverse_transform(self, weights):
        """
        Transform component weights as a 4D dataset.

        Parameters
        ----------
        weights : numpy array of shape [n_samples, n_states + 1]
            The fMRI tseries after projection in the parcellation
            space. Note that the first coefficient corresponds to the intercept,
            and not one of the parcels.

        Returns
        -------
        img : ndarray with a series of images with shape n_samp * n_x * n_y * n_channels
        """
        self._check_components_()
        # add a check on the size of the embedding coefficients
        return self._array2imgs(self.embedding.inverse_transform(weights))

    def compress(self, imgs):
        """
        Provide the approximation of an image after projection in parcellation space.

        Parameters
        ----------
        imgs: ndarray with a series of images.
            imgs size should be n_samp * n_x * n_y * n_channels

        Returns
        -------
        img_c : ndarray.
            The images corresponding to the input, compressed in the parcel space.
        """
        self._check_components_()
        return self.inverse_transform(self.transform(imgs))
