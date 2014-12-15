#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import CaboCha
import re
from collections import defaultdict


class TokenEx:
    """
    tokenクラスを拡張したクラス
    features : [0]品詞 
               [1]品詞細分類1 
               [2]品詞細分類2 
               [3]品詞細分類3 
               [4]活用形 
               [5]活用型 
               [6]原形 
               [7]読み 
               [8]発音
    """
    
    def __init__(self,token):
        self.token = token
        self.features = self.token.feature.split(",")
    
    def to_base(self):
        """
        原型の文字を取得する
        """
        return (self.features[6] != '*' and self.features[6] or self.token.normalized_surface)
    
    def to_s(self):
        return self.token.normalized_surface
    
    def is_noun(self):
        """名詞であるかチェック"""
        return self.features[0] == u'名詞'

    def is_noun_connection(self):
        """名詞接続であるかチェック"""
        return self.features[0] == u'接頭詞' and self.features[1] == u'名詞接続'

    def is_verb(self):
        """動詞であるかチェック"""
        return self.features[0] == u'動詞'

    def is_adjective(self):
        return self.features[0] == u'形容詞'

    def is_sahen_connection(self):
        """サ変接続"""
        return (self.features[0] == u'名詞' and self.features[1] == u'サ変接続')

    def is_sahen_suru(self):
        """サ変・スル"""
        return self.features[4] == u'サ変・スル' 

    def is_sign(self):
        return self.features[0] == u'記号'
    
    def is_setuzoku_joshi(self):
        return (self.features[0] == u'助詞' and self.features[1] == u'接続助詞')

    def is_negative(self):
        return (self.token.normalized_surface == u"ない" and self.features[0] == u'助動詞' and self.features[4] == u'特殊・ナイ') or \
               (self.token.normalized_surface == u"な" and self.features[0] == u'助詞' and self.features[1] == u'終助詞')
    
    def is_command(self):
        return (self.token.normalized_surface == u"な" and self.features[0] == u'助詞' and self.features[1] == u'終助詞') or \
               (self.is_verb() and re.match(u'^[命令]',unicode(self.features[5])) is not None )
        
class ChunkEx:
    def __init__(self,tree,index):
        self.chunk = tree.chunk(index)
        self.tokens = []
        for i in range(self.chunk.token_pos,self.chunk.token_pos + self.chunk.token_size):
            self.tokens.append(TokenEx(tree.token(i)))
    @property
    def link(self):
        return self.chunk.link

    def to_s(self):
        ret = ""
        for t in self.tokens:
            ret += t.to_s()
        return ret

    def is_verb(self):
        """動詞であるか？"""
        return self.tokens[0].is_verb() or self.is_verb_sahen()

    def is_verb_sahen(self):
        """名詞サ変接続＋する"""
        return len(self.tokens) > 1 and self.tokens[0].is_sahen_connection() and self.tokens[1].is_sahen_suru()

    def is_adjective(self):
        return self.tokens[0].is_adjective()

    def is_noun(self):
        """名詞である?"""
        return (not self.is_verb()) and (self.tokens[0].is_noun() or self.tokens[0].is_noun_connection())
        
    def is_subject(self):
        """主語である？"""
        if re.match(u'(^[はもが]$)|^って$',unicode(self.tokens[-1].to_s())) is None:
            return False
        else:
            return self.is_noun() or self.is_adjective() or self.is_verb()

    def is_object(self):
        """目的語である"""
        if re.match(u'(^[をに]$)|^って$',unicode(self.tokens[-1].to_s())) is None:
            return False
        else:
            return self.is_noun() or self.is_adjective() or self.is_verb()
    
    def is_predicte(self):
        """次のリンクが存在しない、または、存在はしているが、現在のチャンクの終わりが接続助詞ならば述語とみなす"""
        if self.link == -1:
            return True

        last_token = None
        for ix in range( len(self.tokens)-1, 0 , -1):
            if not self.tokens[ix].is_sign():
                last_token = self.tokens[ix]
                break
        if last_token is None:
            return False
            
        return last_token.is_setuzoku_joshi()
    
    def is_negative(self):
        """否定形を含むか？"""
        for t in self.tokens:
            if t.is_negative():
                return True
        return False

    def is_command(self):
        """命令形を含むか？"""
        for t in self.tokens:
            if t.is_command():
                return True
        return False
    
    def is_question(self):
        """疑問系か？"""
        return self.tokens[-1].to_s() == "?" or self.tokens[-1].to_s() == "？"

    def to_base(self):
        base = ""
        if self.is_noun():
            # 名詞の場合連続する名詞、・_や名詞接続をくっつける
            for t in self.tokens:
                if t.is_noun_connection():
                    base += t.to_base()
                elif t.is_noun():
                    base += t.to_base()
                elif re.search(u'[＿・]',unicode(t.to_s())) is not None:
                    base += t.to_base()
                elif len(base) > 0:
                    break

        elif self.is_verb_sahen():
            # 名詞サ変接続＋する
            base = self.tokens[0].to_base() + self.tokens[1].to_base()

        elif self.is_verb() or self.is_adjective():
            # 動詞 または形容詞
            base = self.tokens[0].to_base()
        else:
            base = self.to_s()
        
        return base



class CaboChaEx:
    def __init__(self,arg):
        self.p = CaboCha.Parser(arg)
        self.tree = None
        self.chunks = []

    def parse(self,text):
        self.tree = self.p.parse(text)
        self.chunks = []
        for i in range(self.tree.chunk_size()):
            self.chunks.append(ChunkEx(self.tree,i))

    def next_chunk(self,chunk):
        if chunk.link == -1:
            return None
        else:
            return self.chunks[chunk.link]

    def predicte(self):
        """述語の取得."""
        """[基本形:[否定形か？,命令形か？,疑問系か？]"""
        ret = defaultdict(list)
        for c in self.chunks:
            if c.is_predicte():
                ret[c.to_base()] = [c.is_negative(),c.is_command(),c.is_question()]
        return ret

    def subject_predicte_pair(self):
        ret = defaultdict(str)
        for c in self.chunks:
            n = self.next_chunk(c)
            if n is None:
                continue
            if c.is_subject() and n.is_predicte():
                # 主語があって、接続先が存在しないチャンク
                ret[c.to_base()] = n.to_base()
        return ret

    def object_predicte_pair(self):
        ret = defaultdict(str)
        for c in self.chunks:
            n = self.next_chunk(c)
            if n is None:
                continue
            if c.is_object() and n.is_predicte():
                # 目的語があって、接続先が存在しないチャンク
                ret[c.to_base()] = n.to_base()
        return ret

    def pair(self):
        ret = defaultdict(str)
        for c in self.chunks:
            n = self.next_chunk(c)
            if n is None:
                continue
            c_negative = ""
            if c.is_negative():
                c_negative = "-否定"
            n_negative = ""
            if n.is_negative():
                n_negative = "-否定"
            ret[c.to_base() + c_negative] = n.to_base() + n_negative
        return ret
