"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴


"""
from django.db import models
from django.contrib import admin
import logging
import random

logger = logging.getLogger(__name__)

ADVENTURE_CATEGORIES = dict(planetary=1, spatial=2, other=0)
QUESTION_TAGS = ['goal', 'goal', 'goal', 'villain', 'ally', 'patron', 'twist', 'complication', 'sidequest', 'introduction', 'climax', 'framingevent']


class QuizzQuestion(models.Model):
    class Meta:
        ordering = ['num']
    name = models.CharField(max_length=512, blank=True)
    num = models.PositiveIntegerField(default=0)
    subject = models.CharField(max_length=64, default='')
    text = models.CharField(max_length=128, blank=True)
    size = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.num:02}-({self.name}): {self.text}'


class QuizzAnswer(models.Model):
    class Meta:
        ordering = ['question', 'num']
    name = models.CharField(max_length=64, blank=True)
    num = models.PositiveIntegerField(default=0)
    question = models.ForeignKey(QuizzQuestion, on_delete=models.CASCADE)
    text = models.TextField(max_length=512, default='')
    challenge = models.IntegerField(default=1)
    weight = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.num:02}-({self.question.num}): {self.text}'


class Quizz(models.Model):
    from scenarist.models.dramas import Drama
    from scenarist.models.acts import Act
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE, null=True, blank=True)
    act = models.ForeignKey(Act, on_delete=models.CASCADE, null=True, blank=True)
    category = models.PositiveIntegerField(default=ADVENTURE_CATEGORIES['planetary'])
    goal = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='goal')
    villain = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='villain')
    ally = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='ally')
    patron = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='patron')
    twist = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='twist')
    complication = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='complication')
    sidequest = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='side_quest')
    introduction = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='introduction')
    climax = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='climax')
    framingevent = models.ForeignKey(QuizzAnswer, on_delete=models.SET_NULL, blank=True, null=True, related_name='framing_event')

    def __str__(self):
        s = str(self.id)
        if self.drama:
            s = f'{self.drama.full_id} quizz'
        if self.act:
            s = f'{self.act.full_id} quizz'
        return s

    def roll_answer(self, q_num):
        qo = QuizzQuestion.objects.get(num=q_num)
        qo_aos = QuizzAnswer.objects.filter(question=qo)
        odds = []
        for ao in qo_aos:
            for odd in range(ao.weight):
                odds.append(ao.name)
        roll = random.randint(0, len(odds)-1)
        answer = QuizzAnswer.objects.get(name=odds[roll])
        print(f'{qo.text} --> {answer.text}')
        return answer

    # def check_qna(self, pk_q, pk_a):
    #     answer = True
    #     qo = QuizzQuestion.objects.get(pk=pk_q)
    #     ao = QuizzAnswer.objects.get(pk=pk_a)
    #     if ao.question != qo:
    #         answer = False
    #     return answer

    def randomize(self):
        r_category = 1 #random.randint(0, 1)+1
        self.category = r_category
        self.goal = self.roll_answer(self.category)
        self.villain = self.roll_answer(3)
        self.ally = self.roll_answer(4)
        self.patron = self.roll_answer(5)
        self.twist = self.roll_answer(6)
        self.complication = self.roll_answer(7)
        self.sidequest = self.roll_answer(8)
        self.introduction = self.roll_answer(9)
        self.climax = self.roll_answer(10)
        self.framingevent = self.roll_answer(11)

    def verbose_qa(self, q, a):
        t = []
        qo = QuizzQuestion.objects.get(num=q)
        logo = "<i class='fa fa-redo'></i>"
        t.append(f'<div class="topic">')
        t.append(f'<div class="subject">{qo.text}</div>')
        t.append(f'<div class="entry"><button class="quizz" id="quizzx{self.id}_qx{qo.num}_ax{a.num}_{QUESTION_TAGS[qo.num]}" style="margin-left:5ex;width:60ex; font-size:0.9em; padding-left:3ex; text-align:left;">{logo} {a.text}</button></div>')
        t.append(f'</div>')
        return "<br/>".join(t)

    @property
    def verbose(self):
        answer = []
        answer.append(self.verbose_qa(self.category, self.goal))
        answer.append(self.verbose_qa(3, self.villain))
        answer.append(self.verbose_qa(4, self.ally))
        answer.append(self.verbose_qa(5, self.patron))
        answer.append(self.verbose_qa(6, self.twist))
        answer.append(self.verbose_qa(7, self.complication))
        answer.append(self.verbose_qa(8, self.sidequest))
        answer.append(self.verbose_qa(9, self.introduction))
        answer.append(self.verbose_qa(10, self.climax))
        answer.append(self.verbose_qa(11, self.framingevent))
        return "<br/>".join(answer)

    @property
    def ref_id(self):
        s = ""
        if self.drama is not None:
            s = self.drama.full_id
        if self.act is not None:
            s = self.act.full_id
        return s

class QuizzQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'subject', 'name', 'num', 'size']
    search_fields = ['text']
    list_filter = ['text']


class QuizzAnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'num', 'name', 'weight','challenge']
    ordering = ['question', 'num']
    search_fields = ['text']
    list_filter = ['question']


class QuizzAdmin(admin.ModelAdmin):
    list_display = ['__str__','ref_id', 'drama', 'act', 'category', 'goal', 'villain', 'ally', 'patron', 'twist']