import os                                                           as _os

from conway.application.application                                 import Application
from conway.observability.logger                                    import Logger
from conway.util.path_utils                                         import PathUtils

from conway_acceptance.util.test_statics                            import TestStatics

class Test_Logger(Logger):
    '''
    This is a mock logger, needed in order to run the tests of the :class:`conway_test`.

    Specifically, it is needed by the :class:`Chassis_Test_Application`. Please refer to its
    documentation as to why these mock classes are needed in order to run the tests.
    '''


class Chassis_Test_Application(Application):

    '''
    This is a mock application, which is needed in order to run the tests of the :class:`conway_test`.

    This is needed because the :class:`conway` requires that any business logic be run under
    the context of a global :class:`Application` object, which is normally the case for real applications, or 
    for tests of real applications.

    But for testing the :class:`conway` itself without a real application, the tests cases in 
    :class:`conway_test` wouldn't run unless there is (mock) Application as a global context.

    Hence this class, which is initialized in ``conway_test.__init__.py``
    '''
    def __init__(self):

        APP_NAME                                        = "ConwayTestApp"

        # __file__ is something like
        #
        #       /home/alex/consultant1@CCL/dev/conway_fork/conway.test/src/conway_test/framework/application/chassis_test_application.py
        #
        # In that example, the config folder for the Conway test harness would be in 
        #
        #       /home/alex/consultant1@CCL/dev/conway_fork/conway.test/config
        #
        # So we can get that folder by navigating from __file__ the right number of parent directories up
        #
        config_path                                     = PathUtils().n_directories_up(__file__, 4) + "/config"

        logger                                          = Test_Logger(activation_level=Logger.LEVEL_INFO)

        # For ease of use, we want the test harness to be as "auto-configurable" as possible. So we want it
        # to be able to "discover" the location of the test scenarios repo, which normally is under the same
        # parent folder as the repo containing this file. So if the caller has not independently set up the
        # environment variable `TestStatics.SCENARIOS_REPO`, we give it a plausible default value
        # so that tests don't fail to run due to a missing environment variable.
        #
        # This way the caller still has the flexibility of choosing to deploy the scenarios repo 
        # in an unorthodox location and set `TestStatics.SCENARIOS_REPO` to point there. But for
        # most situations, where the scenarios repo is deployed in the "usual place" (i.e., under the same parent folder
        # as the repo containing this file), the default below will forgive callers for "forgetting" to set the environment
        # variable.
        #
        scenarios_repo                                  = _os.environ.get(TestStatics.SCENARIOS_REPO)
        if scenarios_repo is None:
            scenarios_repo                              = PathUtils().n_directories_up(__file__, 5) + "/conway.scenarios"
            logger.log(f"${TestStatics.SCENARIOS_REPO} is not set - defaulting it to {scenarios_repo}",
                       log_level                = 1,
                       stack_level_increase     = 0)
            _os.environ[TestStatics.SCENARIOS_REPO] = scenarios_repo
         
        super().__init__(app_name=APP_NAME, config_path=config_path, logger=logger)

        # Configure the logger to write to the file system in addition to logging to standard output
        # GOTCHA 1:
        #   We do this *after* creating the application instance (i.e., self) since it uses `self.start_time`
        #   which is set in the parent's constructor
        #
        # GOTCHA 2:
        #   Make sure the folder in which the logs are saved is "standard in Linux" for logs, and
        #   that it is a folder accessible to programs that scrape logs, such as Promtail (which feeds Loki/Grafana).
        #   For example, when Promtail runs as a Linux systemd service, by default it runs under a user called
        #   "promtail", wo you want to make sure that user "promtail" has read access to every folder in the path
        #   that goes from the root / all the way to the log file(s)
        #
        # Based on this considerations, we base the path for the logs to be under /var/log but based on the
        # "environment" this application is running under. For that we start with the __file__, which is something like
        #
        #       /home/alex/consultant1@CCL/dev/conway_fork/conway.test/src/conway_test/framework/application/chassis_test_application.py
        #
        #   In this example, the "environment" would be "consultant1@CCL/dev/conway_fork"
        #
        #   After folders are created, you need to give permissions to the user under which this application is run.
        #   Typically that user would be the developer. You also need permissions for the user(s) of scraping
        #   tools, like promtail.
        #
        #   You can recursively give permissions to all such users with something like this, in the above example:
        #
        #       sudo chmod -R 777  /var/log/ccl/consultant1@CCL/dev/conway_fork/ConwayTestApp/
        #

        # end_path is something like "/home/alex/consultant1@CCL/dev/conway_fork"
        #
        end_path                                        = PathUtils().n_directories_up(__file__, 5)
        
        # start_path is something like "/home/alex"
        start_path                                      = PathUtils().n_directories_up(__file__, 8)

        # environment is something like "consultant1@CCL/dev/conway_fork"
        environment                                     = end_path[len(start_path)+1:]

        log_filename                                    = f"{self.start_time}_{APP_NAME}.log"
        #log_file                                        = f"{scenarios_repo}/logs/{log_filename}"
        log_file                                        = f"/var/log/ccl/{environment}/{APP_NAME}/{log_filename}"
        logger.log_file                                 = log_file



