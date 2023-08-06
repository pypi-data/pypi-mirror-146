from Settings import Development, Production, Learn, Staging
import Environment
import Constants

def get():
    return {
        Constants.DEVELOPMENT: Development,
        Constants.PRODUCTION: Production,
        Constants.LEARN: Learn,
        Constants.QA: Staging
    }[Environment.get_environment()]
