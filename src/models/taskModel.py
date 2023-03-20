class Task:
    def __init__(self, userId, taskName, desc,  submissionDate, attachment=None, isTaskComplete=False, isTaskStart=False, isPause=False, startTime=None, lastStartTime=None, endTime=None, spendTime=0):
        self.userId = userId
        self.taskName = taskName
        self.desc = desc
        self.submissionDate = submissionDate
        self.attachment = attachment
        self.isTaskComplete = isTaskComplete
        self.isTaskStart = isTaskStart
        self.isPause = isPause
        self.startTime = startTime
        self.lastStartTime = lastStartTime
        self.endTime = endTime
        self.spendTime = spendTime
