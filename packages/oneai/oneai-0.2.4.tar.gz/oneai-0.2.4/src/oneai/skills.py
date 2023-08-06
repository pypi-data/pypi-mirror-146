from dataclasses import dataclass

from oneai.classes import Skill, skillclass

@skillclass(api_name='enhance', is_generator=True, label_type='replacement', output_attr='enhanced', output_attr1='replacements')
class TranscriptionEnhancer(Skill): pass

@skillclass(api_name='summarize', is_generator=True, label_type='origin', output_attr='summary', output_attr1='origins')
@dataclass
class Summarize(Skill):
    '''
    Provides a summary of the input

    Attributes
    ----------
    min_length : int, default=5
        minimal desired length (words) of the summary 
    max_length : int, default=100
        maximal desired length (words) of the summary 
    find_origins: bool, default=False
        whether to generate origins of the summary, pointing to the input text

    Output
    ------
    Generates an Output object with the summary of the input [and references to the input if find_origins=True].
    Use `.summary.text` for the summary itself, and `.summary.origins` for the references to the input text.

    Examples
    --------
    >>> pipeline = oneai.Pipeline(steps=[
    ...     oneai.skills.Summarize(min_length=10)
    ... ])
    >>> output = pipeline.run('YOUR-TEXT')
    >>> output.summary
    oneai.Output(text='SUMMRY', origins=[...])
    '''
    min_length: int = 5
    max_length: int = 100
    find_origins: bool = True

@skillclass(api_name='emotions', label_type='emotion')
class Emotions(Skill): pass

@skillclass(api_name='entities', label_type='entity')
class Entities(Skill): pass

@skillclass(api_name='keywords', label_type='keyword')
class Keywords(Skill): pass

@skillclass(api_name='highlights', label_type='highlight')
class Highlights(Skill): pass

@skillclass(api_name='sentiments', label_type='sentiment')
class Sentiments(Skill): pass

@skillclass(api_name='article-topics', label_type='topic', output_attr='topics')
class Topics(Skill): pass

@skillclass(api_name='extract-html')
class HTMLExtractArticle(Skill): pass

@skillclass(api_name='html-extract-text')
class HTMLExtractText(Skill): pass

@skillclass(api_name='business-entities', is_generator=True, label_type='business-entity', output_attr='labs', output_attr1='business_entities')
class BusinessEntities(Skill): pass

@skillclass(api_name='action-items', label_type='action-item', output_attr='action_items')
class ActionItems(Skill): pass
