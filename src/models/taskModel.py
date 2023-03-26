class Task:
    def __init__(self, userId, taskName, desc,  submissionDate, attachment=None, isTaskComplete=False, isTaskStart=False, isPause=False, startTime=None, lastStartTime=None, endTime=None, spendTime=0, additionalInfo=None, feedBack=None, submitted=False):
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
        self.additionalInfo = additionalInfo
        self.feedBack = feedBack
        self.submitted = submitted
