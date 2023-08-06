import Settings.Development, Settings.Production, Settings.Learn, Settings.Staging, Settings.Environment, Settings.Constants

def get():
    return {
        Settings.Constants.DEVELOPMENT: Settings.Development,
        Settings.Constants.PRODUCTION: Settings.Production,
        Settings.Constants.LEARN: Settings.Learn,
        Settings.Constants.QA: Settings.Staging
    }[Settings.Environment.get_environment()]
