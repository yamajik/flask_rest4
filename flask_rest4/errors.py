'''Rest4 errors

Errors for Rest4
'''


class InvalidError(Exception):
    def __init__(self, rule):
        message = 'Invalid rule: "{}"'.format(rule)
        super().__init__(message)


class ConflictResourceRule(Exception):
    def __init__(self, rule):
        message = 'Conflict resource rule: "{}"'.format(rule)
        super().__init__(message)
