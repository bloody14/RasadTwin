def test_imports():
    """
    Test that the rasadtwin packages can be imported successfully.
    """
    import rasadtwin
    import rasadtwin.api
    import rasadtwin.explain
    import rasadtwin.forecast
    import rasadtwin.inventory
    import rasadtwin.reopt
    import rasadtwin.routing
    import rasadtwin.sim
    import rasadtwin.utils

    assert rasadtwin is not None
