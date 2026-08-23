import pytest

from cad_bim.adapters.computer_use import HostApplicationRequired, HostJob, run_host_job


def test_host_job_is_explicitly_unavailable(tmp_path) -> None:
    with pytest.raises(HostApplicationRequired, match="IFC4"):
        run_host_job(HostJob(host="revit", model_path=tmp_path / "office.ifc"))
