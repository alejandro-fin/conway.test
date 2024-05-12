

class ConwayTestUtils():

    '''
    Class used to group several helper methods that are used by the Conway tests.
    '''
    def __init__(self):
        pass

    def project_name(scenario_id):
        '''
        Returns the name of the Conway "project" associated to the test case identified by `scenario_id`.

        For example, if `scenario_id` is 8001, then the "project" is `scenario_8001`, which means that
        we expect to see a bundle of repos with names like  `scenario_8001.docs`,  `scenario_8001.svc`,
         `scenario_8001.test`, etc.

        :param int scenario_id: unique identifier of a test case for which we want to know what the corresponding
            project name is.

        :returns: the name of the Conway project for `scenario_id`
        :rtype: str
        '''
        return f"scenario_{scenario_id}"