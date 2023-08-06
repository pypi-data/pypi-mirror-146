def pytest_configure(config):
    config.option.keepduplicates = True


def pytest_collection_modifyitems(session, config, items):
    session = session  # ignore unused var warning

    seen_best_nodes = {}

    for item in items:
        item.prefer_nested_dup_tests__parent_depth = 0
        parent = item.parent
        while parent != None:
            item.prefer_nested_dup_tests__parent_depth = (
                item.prefer_nested_dup_tests__parent_depth + 1
            )
            parent = parent.parent
        if item.nodeid not in seen_best_nodes.keys():
            seen_best_nodes[item.nodeid] = item
        else:
            if (
                item.prefer_nested_dup_tests__parent_depth
                > seen_best_nodes[item.nodeid].prefer_nested_dup_tests__parent_depth
            ):
                seen_best_nodes[item.nodeid] = item

    new_items = list(seen_best_nodes.values())

    items[:] = new_items

    # fix how many items we report in terminal output b/c we do not "deselect" our removed duplicates (intentionally)
    terminal_plugin = config.pluginmanager.get_plugin("terminalreporter")
    terminal_plugin._numcollected = len(items)
    terminal_plugin.report_collect()
