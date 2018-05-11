from model.SQLAlchemy.models.QuestionStatistic import QuestionStatistic
from view.View import View


class LegacyView(View):

    @staticmethod
    def render(obj: QuestionStatistic):
        return {
            'class': 'model.QuestionStatistic.QuestionStatistic',
            'uuid': obj.id,
            'fields': {
                'biggest': obj.biggest,
                'smallest': obj.smallest,
                'q1': obj.q1,
                'q2': obj.q2,
                'q3': obj.q3,
                'answer_count': obj.n
            }
        }
