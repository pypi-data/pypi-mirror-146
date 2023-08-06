from spacy.pipeline import Sentencizer
from spacy.lang.zh import Chinese
from spacy.language import Language
from typing import List, Optional, Tuple, Callable
from spacy.pipeline import Pipe
import spacy


default_punct_chars = ['!',  '?', '։', '؟', '۔', '܀', '܁', '܂', '߹',
            '।', '॥', '၊', '။', '።', '፧', '፨', '᙮', '᜵', '᜶', '᠃', '᠉', '᥄',
            '᥅', '᪨', '᪩', '᪪', '᪫', '᭚', '᭛', '᭞', '᭟', '᰻', '᰼', '᱾', '᱿',
            '‼', '‽', '⁇', '⁈', '⁉', '⸮', '⸼', '꓿', '꘎', '꘏', '꛳', '꛷', '꡶',
            '꡷', '꣎', '꣏', '꤯', '꧈', '꧉', '꩝', '꩞', '꩟', '꫰', '꫱', '꯫', '﹒',
            '﹖', '﹗', '！', '．', '？', '𐩖', '𐩗', '𑁇', '𑁈', '𑂾', '𑂿', '𑃀',
            '𑃁', '𑅁', '𑅂', '𑅃', '𑇅', '𑇆', '𑇍', '𑇞', '𑇟', '𑈸', '𑈹', '𑈻', '𑈼',
            '𑊩', '𑑋', '𑑌', '𑗂', '𑗃', '𑗉', '𑗊', '𑗋', '𑗌', '𑗍', '𑗎', '𑗏', '𑗐',
            '𑗑', '𑗒', '𑗓', '𑗔', '𑗕', '𑗖', '𑗗', '𑙁', '𑙂', '𑜼', '𑜽', '𑜾', '𑩂',
            '𑩃', '𑪛', '𑪜', '𑱁', '𑱂', '𖩮', '𖩯', '𖫵', '𖬷', '𖬸', '𖭄', '𛲟', '𝪈',
            '｡', '。', '？', '！', '......', '……', ';', '；', '.']

@Chinese.factory(name='sentence_segmenter', default_config={'punct_chars': default_punct_chars})
def make_sentence_segmenter(nlp, name, punct_chars):
    return Sentencizer(name, punct_chars=punct_chars)


if __name__ == '__main__':
    nlp = spacy.blank('zh')
    nlp.add_pipe('sentence_segmenter')
    text = "肥厚型心肌病@有阵发性或慢性心房颤动的 HCM 患者使用华法林抗凝的国际标准化比值 (INR) 目标值推荐为 2.0-3.0。"
    doc = nlp(text)
    print(list(doc.sents))

