from codepack import Dependency


def test_eq():
    dependency1 = Dependency(arg='a', id='add3', serial_number='1234')
    dependency2 = Dependency(arg='a', id='add3', serial_number='1234')
    assert dependency1 == dependency2
    dependency_dict2 = dependency2.to_dict()
    assert dependency1 == dependency_dict2
    dependency2.arg = 'b'
    assert dependency1 != dependency2
    assert dependency2 != dependency_dict2
