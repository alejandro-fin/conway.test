from conway.database.single_root_data_hub                               import RelativeDataHubHandle, GitHubDataHubHandle

from conway_ops.database.repos_data_hub                                 import Repos_DataHub
from conway_ops.onboarding.user_profile                                 import UserProfile

from conway_acceptance.scenario_foundry.scenario_manifest               import ScenarioManifest

from conway_test.util.chassis_test_statics                              import Chassis_TestStatics
from conway_test.util.conway_test_utils                                 import ConwayTestUtils

class OperatorScenarioManifest(ScenarioManifest):

    '''
    This is a scenario manifest class used to test functionality of the :class:`conway_ops`
    module. This is functionality intended for an Operator persona whose "job-to-be-done" is around

    * Setting up local and remote repos
    * Managing the flow of commits across branches
    * All of this for a "bundle" of repos associated to a Conway-based project (i.e., the operations are
      not done on a single repo but on a collection of repos).

    The operator is associated to a user profile, that defines the location of the local and remote repos and their
    credentials, if any. 
    Remote repos may be located in either the local file system or on GitHub.

    @param scenarios_root_folder A string representing the absolute path to a folder which serves as the root
        for all test databases across all test scenarios. The test database for which this is a specification
        will be created in `scenarios_root_folder/scenario/`

    @param scenario_id An integer that serves as the unique identifier for the scenario for which this is a
        a specification. A YAML file that maps such numerical ids to the classname of the code that implements
        a test scenario can be found in `scenarios_root_folder/ScenarioIds.yaml`

    '''
    def __init__(self, scenarios_root_folder, scenario_id):
        super().__init__(scenarios_root_folder, scenario_id)

        profile_name                        = Chassis_TestStatics.TEST_USER_PROFILE_NAME
        profile_path                        = f"{self.scenarios_root_folder}/{scenario_id}/SEED@T0/sdlc_root/sdlc.profiles/{profile_name}/profile.toml" 
        self.profile                        = UserProfile(profile_path)

    def get_data_hubs(self):
        '''
        Returns an list of conway.database.data_hub.DataHub objects that define all the DataHubs
        that need to be set up for the test database specific by this Foundry_ScenarioManifest instance.
        '''
        
        local_repos_hub                     = Repos_DataHub(name        = Chassis_TestStatics.BUNDLED_REPOS_LOCAL_FOLDER,
                                                            hub_handle  = RelativeDataHubHandle(
                                                                                self.path_to_actuals(), 
                                                                                Chassis_TestStatics.BUNDLED_REPOS_LOCAL_FOLDER))

        if self.profile.REMOTE_IS_LOCAL():
            remote_repos_hub                = Repos_DataHub(name        = Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER,
                                                            hub_handle  = RelativeDataHubHandle(
                                                                                self.path_to_actuals(), 
                                                                                Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER))
        else:

            remote_repos_hub                = Repos_DataHub(name        = Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER,
                                                            hub_handle  = GitHubDataHubHandle(self.profile))
             

        return [local_repos_hub, remote_repos_hub]
    

    
    
