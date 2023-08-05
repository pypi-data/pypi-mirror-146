import napari
import numpy as np
import pytest
from scipy.ndimage import rotate
from stardist.models import StarDist2D, StarDist3D

from .._dock_widget import CUSTOM_MODEL, Output, TimelapseLabels


def test_fluo_2d(plugin, nuclei_2d):
    kwargs = dict(viewer=None, image=nuclei_2d, axes="YX")

    for output_type, num_out in (
        (Output.Labels.value, 1),
        (Output.Polys.value, 1),
        (Output.Both.value, 2),
    ):
        out = plugin(
            **kwargs,
            output_type=output_type,
        )
        assert len(out) == num_out

    out = plugin(
        **kwargs,
        input_scale=0.75,
        cnn_output=True,
        n_tiles=(3, 2),
    )
    assert len(out) == 4


def test_fluo_3d(plugin, nuclei_3d):
    kwargs = dict(viewer=None, image=nuclei_3d, axes="ZYX", model_type=StarDist3D)

    for output_type, num_out in (
        (Output.Labels.value, 1),
        (Output.Polys.value, 1),
        (Output.Both.value, 2),
    ):
        out = plugin(
            **kwargs,
            output_type=output_type,
        )
        assert len(out) == num_out

    out = plugin(
        **kwargs,
        input_scale=0.75,
        cnn_output=True,
        n_tiles=(2, 1, 2),
    )
    assert len(out) == 4


def test_custom_model_2d(plugin, nuclei_2d):
    from csbdeep.models.pretrained import get_model_folder

    model_type = StarDist2D
    model_name = "2D_versatile_fluo"
    model_path = get_model_folder(model_type, model_name)

    kwargs = dict(viewer=None, image=nuclei_2d, axes="YX")
    labels1, polys1 = plugin(**kwargs, model_type=model_type, model2d=model_name)
    labels2, polys2 = plugin(**kwargs, model_type=CUSTOM_MODEL, model_folder=model_path)

    assert np.allclose(labels1[0], labels2[0]) and labels1[1] == labels2[1]
    assert np.allclose(polys1[0], polys2[0]) and polys1[1] == polys2[1]


def test_timelapse_2d(plugin, nuclei_2d):
    timelapse = np.stack(
        [
            rotate(nuclei_2d.data, deg, reshape=False, mode="reflect")
            for deg in np.linspace(0, 50, 3)
        ],
        axis=0,
    )
    timelapse = napari.layers.Image(timelapse, name="timelapse")
    kwargs = dict(viewer=None, image=timelapse, axes="TYX")

    for t in TimelapseLabels:
        plugin(**kwargs, timelapse_opts=t.value)

    out = plugin(**kwargs, cnn_output=True)
    assert len(out) == 4

    out = plugin(**kwargs, n_tiles=(1, 2, 3))
    assert len(out) == 2


def test_timelapse_3d(plugin, nuclei_3d):
    timelapse = np.stack([np.roll(nuclei_3d.data, n) for n in (0, 10)], axis=0)
    timelapse = napari.layers.Image(timelapse, name="timelapse")
    kwargs = dict(viewer=None, image=timelapse, axes="TZYX", model_type=StarDist3D)

    with pytest.raises(NotImplementedError):
        plugin(**kwargs, output_type=Output.Polys.value)

    kwargs["output_type"] = Output.Labels.value

    for t in TimelapseLabels:
        plugin(**kwargs, timelapse_opts=t.value)

    out = plugin(**kwargs, cnn_output=True)
    assert len(out) == 3

    out = plugin(**kwargs, n_tiles=(1, 1, 2, 3))
    assert len(out) == 1


def test_he_2d(plugin, he_2d):
    kwargs = dict(viewer=None, image=he_2d, axes="YXC", model2d="2D_versatile_he")

    out = plugin(**kwargs)
    assert len(out) == 2
