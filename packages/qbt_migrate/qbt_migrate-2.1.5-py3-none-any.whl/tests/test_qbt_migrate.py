from qbt_migrate import FastResume, QBTBatchMove, convert_slashes, valid_path


def test_convert_slashes():
    path = 'C:\\This\\is\\a\\windows\\path'
    assert convert_slashes(path, 'Windows') == path
    assert convert_slashes(path, 'Linux') == path.replace('\\', '/')

    path = '/this/is/a/nix/path'
    assert convert_slashes(path, 'Linux') == path
    assert convert_slashes(path, 'Windows') == path.replace('/', '\\')
