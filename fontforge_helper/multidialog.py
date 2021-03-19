from collections.abc import Hashable
from enum import Enum
import abc
from copy import deepcopy

class MultiAnswer(dict):
    @property
    def default(self):
        return super().get('default', False)

    @default.setter
    def default(self, v):
        if v:
            super().__setitem__('default', True)
        else:
            super().pop('default', None)

    @property
    def name(self):
        return super().get('name')
    
    @name.setter
    def name(self, v):
        if not isinstance(v, str):
            raise ValueError("Answer name must be a string")
        super().__setitem__('name', v)

    @property
    def tag(self, v):
        return super().get('tag', None)

    @tag.setter
    def tag(self, v):
        if v is not None:
            super().__setitem__('tag', v)
        else:
            super().pop('tag', None)
    
    def __init__(self, name, tag=None, default=False):
        self.name = name
        self.tag = tag
        self.default = default

class _MultiQuestion(dict, abc.ABC):
    class Type(Enum):
        OPENPATH = 'openpath'
        SAVEPATH = 'savepath'
        STRING = 'string'
        CHOICE = 'choice'

    @property
    def type(self):
        return _MultiQuestion.Type(super().get('type'))

    @property
    def label(self):
        return super().get('question')

    @label.setter
    def label(self, v):
        if not isinstance(v, str) and v is not None:
            raise ValueError("Question label must be a string or None")
        super().__setitem__('question', v)

    @property
    def tag(self, v):
        return super().get('tag', None)

    @tag.setter
    def tag(self, v):
        if v is None:
            super().pop('tag', None)
        elif not isinstance(v, Hashable):
            raise TypeError("Question tag must be hashable")
        else:
            super().__setitem__('tag', v)
   
    @property
    def align(self):
        return super().get('align', True)

    @align.setter
    def align(self, v):
        if not v:
            super().__setitem__('noalign', True)
        else:
            super().pop('noalign', None)

    @abc.abstractmethod
    def __init__(self, qtype, label, tag, align):
        super().__init__()
        if not isinstance(qtype, _MultiQuestion.Type):
            raise TypeError('qtype is not a MultiQuestion.Type')
        super().__setitem__('type', qtype.value)
        self.label = label
        self.tag = tag
        self.align = align

class _MultiQuestionStrDefault(_MultiQuestion):
    @property
    def default(self):
        return super().get('default', None)

    @default.setter
    def default(self, v):
        if v is None:
            super().pop('default', None)
        if not isinstance(v, str):
            raise ValueError("Question default must be a string")
        super().__setitem__('default', v)

    @abc.abstractmethod
    def __init__(self, qtype, label, default, tag, align):
        super().__init__(qtype, label, tag, align)
        self.default = default

class _MultiQuestionFilter(_MultiQuestionStrDefault):
    @property
    def fltr(self):
        return super().get('filter', None)

    @fltr.setter
    def fltr(self, v):
        if v is None:
            super().pop('filter', None)
        if not isinstance(v, str):
            raise ValueError("File chooser filter must be a string")
        super().__setitem__('filter', v)

    @abc.abstractmethod
    def __init__(self, qtype, label, default, fltr, tag, align):
        super().__init__(qtype, label, default, tag, align)
        self.fltr = fltr

class MultiChoice(_MultiQuestion):
    @property
    def multiple(self):
        return super().get('multiple', False)

    @multiple.setter
    def multiple(self, v):
        if v:
            super().__setitem__('multiple', True)
        else:
            super().pop('multiple', None)

    @property
    def checks(self):
        return super().get('checks', False)

    @checks.setter
    def checks(self, v):
        if v:
            super().__setitem__('checks', True)
        else:
            super().pop('checks', None)

    def get_answers(self):
        return deepcopy(super().get('answers'))

    def set_answers(self, v):
        err = False
        if not instanceof(v, list):
            err = True
        else:
            for a in v:
                if not instanceof(a, MultiAnswer):
                    err = True
                    break
        if err:
            raise TypeError('answers value must be list of MultiAnswer objects')
        super().__setitem__('answers', deepcopy(v))

    def add_answer(self, a):
        if not isinstance(a, MultiAnswer):
            raise Error("Only a MultiAnswer can be added")
        super().get('answers').append(deepcopy(a))

    def __init__(self, label, multiple=False, checks=False, tag=None, align=True):
        super().__init__(_MultiQuestion.Type.CHOICE, label, tag, align)
        super().__setitem__('answers', [])
        self.multiple = multiple
        self.checks = checks

class MultiString(_MultiQuestionStrDefault):
    def __init__(self, label, default=None, tag=None, align=True):
        super().__init__(_MultiQuestion.Type.STRING, label, default, tag, align)

class MultiSave(_MultiQuestionFilter):
    def __init__(self, label, default=None, fltr=None, tag=None, align=True):
        super().__init__(_MultiQuestion.Type.SAVEPATH, label, default, fltr, tag, align)

class MultiOpen(_MultiQuestionFilter):
    def __init__(self, label, default=None, fltr=None, tag=None, align=True):
        super().__init__(_MultiQuestion.Type.OPENPATH, label, default, fltr, tag, align)

class MultiCategory(dict):
    @property
    def label(self):
        return super().get('category')

    @label.setter
    def label(self, v):
        if not isinstance(v, str) and v is not None:
            raise ValueError("Category label must be a string or None")
        super().__setitem__('category', v)
    
    def get_questions(self):
        return deepcopy(super().get('questions'))

    def set_questions(self, v):
        err = False
        if not instanceof(v, list):
            err = True
        else:
            for a in v:
                if not instanceof(a, _MultiQuestion):
                    err = True
                    break
        if err:
            raise TypeError('questions value must be list of MultiQuestion objects (MultiChoice, MultiString, MultiOpen or MultiSave)')
        super().__setitem__('questions', deepcopy(v))

    def add_question(self, q):
        if not isinstance(q, _MultiQuestion):
            raise TypeError("Only a MultiQuestion (MultiChoice, MultiString, MultiOpen or MultiSave) can be added")
        super().get('questions').append(deepcopy(q))

    def __init__(self, label):
        super().__init__()
        super().__setitem__('questions', [])
        self.label = label;

class MultiDialog(list):
    def get_categories(self):
        return super().copy()

    def set_categories(self, v):
        err = False
        if not instanceof(v, list):
            err = True
        else:
            for a in v:
                if not instanceof(a, MultiCategory):
                    err = True
                    break
        if err:
            raise TypeError('categories value must be list of MultiCategory objects')
        super().clear()
        super().extend(v)

    def add_category(self, c):
        if not isinstance(c, MultiCategory):
            raise TypeError("Only a MultiCategory can be added")
        super().append(deepcopy(c))

    def __init__(self):
        super().__init__()
