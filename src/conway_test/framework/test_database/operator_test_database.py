from conway.database.single_root_data_hub                                      import RelativeDataHubHandle

from conway_ops.database.repos_data_hub                                        import Repos_DataHub

from conway_test.util.chassis_test_statics                                     import Chassis_TestStatics

from conway_acceptance.test_database.test_database                                         import TestDatabase


class Operator_TestDatabase(TestDatabase):

    def __init__(self, manifest):
        '''
        :param OperatorScenarioManifest manifest: Object that has connection strings to access the test database that 
            should be used by the test case using this OperatorTestDatabase.
        '''
        super().__init__(manifest)

        [local_repos_hub, remote_repos_hub]                         = manifest.get_data_hubs()

        self.local_repos_hub                                        = local_repos_hub
        self.remote_repos_hub                                       = remote_repos_hub
    
    def populate_from_seed(self):
        '''
        Uses the data in seeds to initialize the contents of the database. If any prior contents exist, they will be removed.
        '''
        seed_folder                                                 = self.manifest.path_to_seed()

        self.local_repos_hub.populate_from_seed(Repos_DataHub(
                                                name        = Chassis_TestStatics.BUNDLED_REPOS_LOCAL_FOLDER,
                                                hub_handle  = RelativeDataHubHandle(seed_folder, 
                                                                                    Chassis_TestStatics.BUNDLED_REPOS_LOCAL_FOLDER)))
        if self.manifest.profile.REMOTE_IS_LOCAL():
            self.remote_repos_hub.populate_from_seed(Repos_DataHub(
                                                name        = Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER, 
                                                hub_handle  = RelativeDataHubHandle(seed_folder, 
                                                                                    Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER)))


    def enrich_from_seed(self, seeding_round):
        '''
        Uses the data in seeds to enrich the contents of the database.

        @param seeding_round An int, designating the round fo seeding for which we seek the path.
                By default it is 0, so it returns a path to a folder called "SEED@T0". For some test cases that is the
                only seeding event in the lifecycle of the test, but other test cases require multiple phases where
                at each phase we need to simulate that the user has changed or added additional
                content to the database. In that case, the test harness pattern calls for multiple seeding events each of
                which will enrich the database at different times from data in different folders. For example,
                a folder "SEED@T0" would be used for an initial seeding at the start of the test,
                then "SEED@T1" for content that must be used to enrich the database in a subsequent phase 1, then
                "SEED@T2" for a subsequent phase 2, etc.

        '''
        seed_folder                                                 = self.manifest.path_to_seed(seeding_round)

        self.local_repos_hub.enrich_from_seed(Repos_DataHub(
                                                name        = Chassis_TestStatics.BUNDLED_REPOS_LOCAL_FOLDER,
                                                hub_handle  = RelativeDataHubHandle(seed_folder, 
                                                                                    Chassis_TestStatics.BUNDLED_REPOS_LOCAL_FOLDER)))
        
        if self.manifest.profile.REMOTE_IS_LOCAL():
            self.remote_repos_hub.enrich_from_seed(Repos_DataHub(
                                                name        = Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER, 
                                                hub_handle  = RelativeDataHubHandle(seed_folder, 
                                                                                    Chassis_TestStatics.BUNDLED_REPOS_REMOTE_FOLDER)))


        