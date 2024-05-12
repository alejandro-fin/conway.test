
from conway_ops.onboarding.repo_bundle                      import RepoBundle
from conway_ops.repo_admin.repo_statics                     import RepoStatics
from conway_ops.repo_admin.repo_administration              import RepoAdministration

from conway_acceptance.test_logic.excels_to_compare         import ExcelsToCompare, WorksheetComparisonInfo


class Chassis_ExcelsToCompare(ExcelsToCompare):

    def __init__(self):
        super().__init__()

    PUBLICATIONS                                            = "/" + RepoStatics.OPERATOR_REPORTS

    XL_REPO_STATS                                           = RepoStatics.REPORT_REPO_STATS + ".xlsx"

    def addXL_RepoStats(self, project_name):
        '''
        Adds the "RepoStats.xlsx" Excel
        '''
        XL                                                  = self._REPOS() + self.XL_REPO_STATS

        worksheets                                          = [RepoStatics.REPORT_REPO_STATS_WORKSHEET]

        # Figure out the log worksheets
        repo_info_l                                         = RepoBundle(project_name).bundled_repos()
        repo_names                                          = [info.name for info in repo_info_l]
        for n in repo_names:
            worksheets.append(RepoAdministration.worksheet_for_log(n, RepoStatics.LOCAL_REPO))
            worksheets.append(RepoAdministration.worksheet_for_log(n, RepoStatics.REMOTE_REPO))

        self.addXL(XL, self._WS_INFO(worksheets))


    def _REPOS(self):
        '''
        Abbreviating method for the prefix that is common in the relative path of Governance reports
        '''
        return self.PUBLICATIONS + "/" + RepoStatics.DEV_OPS_REPORTS_FOLDER + "/" 
    

    def _WS_INFO(self, worksheet_name_l, is_optional=False):
        '''
        Helper method to turn a list of strings representing worksheet names into a list of 
        WorksheetComparisonInfo objects that can be added into an ExcelToCompare object.
        '''
        info_l                                              = [WorksheetComparisonInfo(w, is_optional) for w in worksheet_name_l]
        return info_l