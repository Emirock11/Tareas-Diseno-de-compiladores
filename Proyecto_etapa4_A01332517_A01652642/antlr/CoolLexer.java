// Generated from .\Cool.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class CoolLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, KLASS=2, FI=3, IF=4, IN=5, INHERITS=6, ISVOID=7, LET=8, LOOP=9, 
		POOL=10, THEN=11, ELSE=12, WHILE=13, CASE=14, ESAC=15, NEW=16, OF=17, 
		NOT=18, TRUE=19, FALSE=20, TYPE=21, ID=22, INTEGER=23, STRING=24, COMMENT=25, 
		LINE_COMENT=26, WHITESPACE=27, LPAR=28, RPAR=29, LBRA=30, RBRA=31, COMMA=32, 
		COLON=33, SEMICOLON=34, CASEASSIGN=35, MULT=36, DIV=37, ADD=38, SUB=39, 
		EQUAL=40, TWODASHES=41, INTCOMP=42, LT=43, LE=44, ASSIGN=45, AT=46;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
			"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "KLASS", 
			"FI", "IF", "IN", "INHERITS", "ISVOID", "LET", "LOOP", "POOL", "THEN", 
			"ELSE", "WHILE", "CASE", "ESAC", "NEW", "OF", "NOT", "TRUE", "FALSE", 
			"TYPE", "ID", "INTEGER", "STRING", "COMMENT", "LINE_COMENT", "WHITESPACE", 
			"LPAR", "RPAR", "LBRA", "RBRA", "COMMA", "COLON", "SEMICOLON", "CASEASSIGN", 
			"MULT", "DIV", "ADD", "SUB", "EQUAL", "TWODASHES", "INTCOMP", "LT", "LE", 
			"ASSIGN", "AT"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'.'", null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, "'('", "')'", "'{'", "'}'", "','", "':'", "';'", 
			"'=>'", "'*'", "'/'", "'+'", "'-'", "'='", "'--'", "'~'", "'<'", "'<='", 
			"'<-'", "'@'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, "KLASS", "FI", "IF", "IN", "INHERITS", "ISVOID", "LET", "LOOP", 
			"POOL", "THEN", "ELSE", "WHILE", "CASE", "ESAC", "NEW", "OF", "NOT", 
			"TRUE", "FALSE", "TYPE", "ID", "INTEGER", "STRING", "COMMENT", "LINE_COMENT", 
			"WHITESPACE", "LPAR", "RPAR", "LBRA", "RBRA", "COMMA", "COLON", "SEMICOLON", 
			"CASEASSIGN", "MULT", "DIV", "ADD", "SUB", "EQUAL", "TWODASHES", "INTCOMP", 
			"LT", "LE", "ASSIGN", "AT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public CoolLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "Cool.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\60\u0194\b\1\4\2"+
		"\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4"+
		"\13\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22"+
		"\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31"+
		"\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t"+
		" \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t"+
		"+\4,\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64"+
		"\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t"+
		"=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4"+
		"I\tI\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3"+
		"\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20\3\21\3"+
		"\21\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3"+
		"\30\3\31\3\31\3\32\3\32\3\33\3\33\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3"+
		"\35\3\36\3\36\3\36\3\37\3\37\3\37\3 \3 \3 \3!\3!\3!\3!\3!\3!\3!\3!\3!"+
		"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%\3"+
		"%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3(\3)\3)\3)\3)\3)"+
		"\3*\3*\3*\3*\3*\3+\3+\3+\3+\3,\3,\3,\3-\3-\3-\3-\3.\3.\3.\3.\3.\3/\3/"+
		"\3/\3/\3/\3/\3\60\3\60\7\60\u0129\n\60\f\60\16\60\u012c\13\60\3\61\3\61"+
		"\7\61\u0130\n\61\f\61\16\61\u0133\13\61\3\62\6\62\u0136\n\62\r\62\16\62"+
		"\u0137\3\63\3\63\3\63\3\63\3\63\3\63\3\63\5\63\u0141\n\63\3\63\7\63\u0144"+
		"\n\63\f\63\16\63\u0147\13\63\3\63\3\63\3\64\3\64\3\64\3\64\7\64\u014f"+
		"\n\64\f\64\16\64\u0152\13\64\3\64\3\64\3\64\3\64\3\64\3\65\3\65\3\65\3"+
		"\65\7\65\u015d\n\65\f\65\16\65\u0160\13\65\3\65\3\65\3\66\6\66\u0165\n"+
		"\66\r\66\16\66\u0166\3\66\3\66\3\67\3\67\38\38\39\39\3:\3:\3;\3;\3<\3"+
		"<\3=\3=\3>\3>\3>\3?\3?\3@\3@\3A\3A\3B\3B\3C\3C\3D\3D\3D\3E\3E\3F\3F\3"+
		"G\3G\3G\3H\3H\3H\3I\3I\3\u0150\2J\3\3\5\2\7\2\t\2\13\2\r\2\17\2\21\2\23"+
		"\2\25\2\27\2\31\2\33\2\35\2\37\2!\2#\2%\2\'\2)\2+\2-\2/\2\61\2\63\2\65"+
		"\2\67\29\4;\5=\6?\7A\bC\tE\nG\13I\fK\rM\16O\17Q\20S\21U\22W\23Y\24[\25"+
		"]\26_\27a\30c\31e\32g\33i\34k\35m\36o\37q s!u\"w#y${%}&\177\'\u0081(\u0083"+
		")\u0085*\u0087+\u0089,\u008b-\u008d.\u008f/\u0091\60\3\2$\4\2CCcc\4\2"+
		"DDdd\4\2EEee\4\2FFff\4\2GGgg\4\2HHhh\4\2IIii\4\2JJjj\4\2KKkk\4\2LLll\4"+
		"\2MMmm\4\2NNnn\4\2OOoo\4\2PPpp\4\2QQqq\4\2RRrr\4\2SSss\4\2TTtt\4\2UUu"+
		"u\4\2VVvv\4\2WWww\4\2XXxx\4\2YYyy\4\2ZZzz\4\2[[{{\4\2\\\\||\3\2C\\\6\2"+
		"\62;C\\aac|\4\2aac|\3\2\62;\4\2\13\13^^\4\2\f\f\17\17\6\2\13\f\17\17$"+
		"$^^\5\2\13\f\16\17\"\"\2\u0184\2\3\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3"+
		"\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2"+
		"\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2"+
		"W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3"+
		"\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2"+
		"\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2"+
		"}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2"+
		"\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f"+
		"\3\2\2\2\2\u0091\3\2\2\2\3\u0093\3\2\2\2\5\u0095\3\2\2\2\7\u0097\3\2\2"+
		"\2\t\u0099\3\2\2\2\13\u009b\3\2\2\2\r\u009d\3\2\2\2\17\u009f\3\2\2\2\21"+
		"\u00a1\3\2\2\2\23\u00a3\3\2\2\2\25\u00a5\3\2\2\2\27\u00a7\3\2\2\2\31\u00a9"+
		"\3\2\2\2\33\u00ab\3\2\2\2\35\u00ad\3\2\2\2\37\u00af\3\2\2\2!\u00b1\3\2"+
		"\2\2#\u00b3\3\2\2\2%\u00b5\3\2\2\2\'\u00b7\3\2\2\2)\u00b9\3\2\2\2+\u00bb"+
		"\3\2\2\2-\u00bd\3\2\2\2/\u00bf\3\2\2\2\61\u00c1\3\2\2\2\63\u00c3\3\2\2"+
		"\2\65\u00c5\3\2\2\2\67\u00c7\3\2\2\29\u00c9\3\2\2\2;\u00cf\3\2\2\2=\u00d2"+
		"\3\2\2\2?\u00d5\3\2\2\2A\u00d8\3\2\2\2C\u00e1\3\2\2\2E\u00e8\3\2\2\2G"+
		"\u00ec\3\2\2\2I\u00f1\3\2\2\2K\u00f6\3\2\2\2M\u00fb\3\2\2\2O\u0100\3\2"+
		"\2\2Q\u0106\3\2\2\2S\u010b\3\2\2\2U\u0110\3\2\2\2W\u0114\3\2\2\2Y\u0117"+
		"\3\2\2\2[\u011b\3\2\2\2]\u0120\3\2\2\2_\u0126\3\2\2\2a\u012d\3\2\2\2c"+
		"\u0135\3\2\2\2e\u0139\3\2\2\2g\u014a\3\2\2\2i\u0158\3\2\2\2k\u0164\3\2"+
		"\2\2m\u016a\3\2\2\2o\u016c\3\2\2\2q\u016e\3\2\2\2s\u0170\3\2\2\2u\u0172"+
		"\3\2\2\2w\u0174\3\2\2\2y\u0176\3\2\2\2{\u0178\3\2\2\2}\u017b\3\2\2\2\177"+
		"\u017d\3\2\2\2\u0081\u017f\3\2\2\2\u0083\u0181\3\2\2\2\u0085\u0183\3\2"+
		"\2\2\u0087\u0185\3\2\2\2\u0089\u0188\3\2\2\2\u008b\u018a\3\2\2\2\u008d"+
		"\u018c\3\2\2\2\u008f\u018f\3\2\2\2\u0091\u0192\3\2\2\2\u0093\u0094\7\60"+
		"\2\2\u0094\4\3\2\2\2\u0095\u0096\t\2\2\2\u0096\6\3\2\2\2\u0097\u0098\t"+
		"\3\2\2\u0098\b\3\2\2\2\u0099\u009a\t\4\2\2\u009a\n\3\2\2\2\u009b\u009c"+
		"\t\5\2\2\u009c\f\3\2\2\2\u009d\u009e\t\6\2\2\u009e\16\3\2\2\2\u009f\u00a0"+
		"\t\7\2\2\u00a0\20\3\2\2\2\u00a1\u00a2\t\b\2\2\u00a2\22\3\2\2\2\u00a3\u00a4"+
		"\t\t\2\2\u00a4\24\3\2\2\2\u00a5\u00a6\t\n\2\2\u00a6\26\3\2\2\2\u00a7\u00a8"+
		"\t\13\2\2\u00a8\30\3\2\2\2\u00a9\u00aa\t\f\2\2\u00aa\32\3\2\2\2\u00ab"+
		"\u00ac\t\r\2\2\u00ac\34\3\2\2\2\u00ad\u00ae\t\16\2\2\u00ae\36\3\2\2\2"+
		"\u00af\u00b0\t\17\2\2\u00b0 \3\2\2\2\u00b1\u00b2\t\20\2\2\u00b2\"\3\2"+
		"\2\2\u00b3\u00b4\t\21\2\2\u00b4$\3\2\2\2\u00b5\u00b6\t\22\2\2\u00b6&\3"+
		"\2\2\2\u00b7\u00b8\t\23\2\2\u00b8(\3\2\2\2\u00b9\u00ba\t\24\2\2\u00ba"+
		"*\3\2\2\2\u00bb\u00bc\t\25\2\2\u00bc,\3\2\2\2\u00bd\u00be\t\26\2\2\u00be"+
		".\3\2\2\2\u00bf\u00c0\t\27\2\2\u00c0\60\3\2\2\2\u00c1\u00c2\t\30\2\2\u00c2"+
		"\62\3\2\2\2\u00c3\u00c4\t\31\2\2\u00c4\64\3\2\2\2\u00c5\u00c6\t\32\2\2"+
		"\u00c6\66\3\2\2\2\u00c7\u00c8\t\33\2\2\u00c88\3\2\2\2\u00c9\u00ca\5\t"+
		"\5\2\u00ca\u00cb\5\33\16\2\u00cb\u00cc\5\5\3\2\u00cc\u00cd\5)\25\2\u00cd"+
		"\u00ce\5)\25\2\u00ce:\3\2\2\2\u00cf\u00d0\5\17\b\2\u00d0\u00d1\5\25\13"+
		"\2\u00d1<\3\2\2\2\u00d2\u00d3\5\25\13\2\u00d3\u00d4\5\17\b\2\u00d4>\3"+
		"\2\2\2\u00d5\u00d6\5\25\13\2\u00d6\u00d7\5\37\20\2\u00d7@\3\2\2\2\u00d8"+
		"\u00d9\5\25\13\2\u00d9\u00da\5\37\20\2\u00da\u00db\5\23\n\2\u00db\u00dc"+
		"\5\r\7\2\u00dc\u00dd\5\'\24\2\u00dd\u00de\5\25\13\2\u00de\u00df\5+\26"+
		"\2\u00df\u00e0\5)\25\2\u00e0B\3\2\2\2\u00e1\u00e2\5\25\13\2\u00e2\u00e3"+
		"\5)\25\2\u00e3\u00e4\5/\30\2\u00e4\u00e5\5!\21\2\u00e5\u00e6\5\25\13\2"+
		"\u00e6\u00e7\5\13\6\2\u00e7D\3\2\2\2\u00e8\u00e9\5\33\16\2\u00e9\u00ea"+
		"\5\r\7\2\u00ea\u00eb\5+\26\2\u00ebF\3\2\2\2\u00ec\u00ed\5\33\16\2\u00ed"+
		"\u00ee\5!\21\2\u00ee\u00ef\5!\21\2\u00ef\u00f0\5#\22\2\u00f0H\3\2\2\2"+
		"\u00f1\u00f2\5#\22\2\u00f2\u00f3\5!\21\2\u00f3\u00f4\5!\21\2\u00f4\u00f5"+
		"\5\33\16\2\u00f5J\3\2\2\2\u00f6\u00f7\5+\26\2\u00f7\u00f8\5\23\n\2\u00f8"+
		"\u00f9\5\r\7\2\u00f9\u00fa\5\37\20\2\u00faL\3\2\2\2\u00fb\u00fc\5\r\7"+
		"\2\u00fc\u00fd\5\33\16\2\u00fd\u00fe\5)\25\2\u00fe\u00ff\5\r\7\2\u00ff"+
		"N\3\2\2\2\u0100\u0101\5\61\31\2\u0101\u0102\5\23\n\2\u0102\u0103\5\25"+
		"\13\2\u0103\u0104\5\33\16\2\u0104\u0105\5\r\7\2\u0105P\3\2\2\2\u0106\u0107"+
		"\5\t\5\2\u0107\u0108\5\5\3\2\u0108\u0109\5)\25\2\u0109\u010a\5\r\7\2\u010a"+
		"R\3\2\2\2\u010b\u010c\5\r\7\2\u010c\u010d\5)\25\2\u010d\u010e\5\5\3\2"+
		"\u010e\u010f\5\t\5\2\u010fT\3\2\2\2\u0110\u0111\5\37\20\2\u0111\u0112"+
		"\5\r\7\2\u0112\u0113\5\61\31\2\u0113V\3\2\2\2\u0114\u0115\5!\21\2\u0115"+
		"\u0116\5\17\b\2\u0116X\3\2\2\2\u0117\u0118\5\37\20\2\u0118\u0119\5!\21"+
		"\2\u0119\u011a\5+\26\2\u011aZ\3\2\2\2\u011b\u011c\5+\26\2\u011c\u011d"+
		"\5\'\24\2\u011d\u011e\5-\27\2\u011e\u011f\5\r\7\2\u011f\\\3\2\2\2\u0120"+
		"\u0121\5\17\b\2\u0121\u0122\5\5\3\2\u0122\u0123\5\33\16\2\u0123\u0124"+
		"\5)\25\2\u0124\u0125\5\r\7\2\u0125^\3\2\2\2\u0126\u012a\t\34\2\2\u0127"+
		"\u0129\t\35\2\2\u0128\u0127\3\2\2\2\u0129\u012c\3\2\2\2\u012a\u0128\3"+
		"\2\2\2\u012a\u012b\3\2\2\2\u012b`\3\2\2\2\u012c\u012a\3\2\2\2\u012d\u0131"+
		"\t\36\2\2\u012e\u0130\t\35\2\2\u012f\u012e\3\2\2\2\u0130\u0133\3\2\2\2"+
		"\u0131\u012f\3\2\2\2\u0131\u0132\3\2\2\2\u0132b\3\2\2\2\u0133\u0131\3"+
		"\2\2\2\u0134\u0136\t\37\2\2\u0135\u0134\3\2\2\2\u0136\u0137\3\2\2\2\u0137"+
		"\u0135\3\2\2\2\u0137\u0138\3\2\2\2\u0138d\3\2\2\2\u0139\u0145\7$\2\2\u013a"+
		"\u0141\t \2\2\u013b\u013c\7\17\2\2\u013c\u0141\7\f\2\2\u013d\u0141\t!"+
		"\2\2\u013e\u013f\7^\2\2\u013f\u0141\7$\2\2\u0140\u013a\3\2\2\2\u0140\u013b"+
		"\3\2\2\2\u0140\u013d\3\2\2\2\u0140\u013e\3\2\2\2\u0141\u0144\3\2\2\2\u0142"+
		"\u0144\n\"\2\2\u0143\u0140\3\2\2\2\u0143\u0142\3\2\2\2\u0144\u0147\3\2"+
		"\2\2\u0145\u0143\3\2\2\2\u0145\u0146\3\2\2\2\u0146\u0148\3\2\2\2\u0147"+
		"\u0145\3\2\2\2\u0148\u0149\7$\2\2\u0149f\3\2\2\2\u014a\u014b\7*\2\2\u014b"+
		"\u014c\7,\2\2\u014c\u0150\3\2\2\2\u014d\u014f\13\2\2\2\u014e\u014d\3\2"+
		"\2\2\u014f\u0152\3\2\2\2\u0150\u0151\3\2\2\2\u0150\u014e\3\2\2\2\u0151"+
		"\u0153\3\2\2\2\u0152\u0150\3\2\2\2\u0153\u0154\7,\2\2\u0154\u0155\7+\2"+
		"\2\u0155\u0156\3\2\2\2\u0156\u0157\b\64\2\2\u0157h\3\2\2\2\u0158\u0159"+
		"\7/\2\2\u0159\u015a\7/\2\2\u015a\u015e\3\2\2\2\u015b\u015d\n!\2\2\u015c"+
		"\u015b\3\2\2\2\u015d\u0160\3\2\2\2\u015e\u015c\3\2\2\2\u015e\u015f\3\2"+
		"\2\2\u015f\u0161\3\2\2\2\u0160\u015e\3\2\2\2\u0161\u0162\b\65\2\2\u0162"+
		"j\3\2\2\2\u0163\u0165\t#\2\2\u0164\u0163\3\2\2\2\u0165\u0166\3\2\2\2\u0166"+
		"\u0164\3\2\2\2\u0166\u0167\3\2\2\2\u0167\u0168\3\2\2\2\u0168\u0169\b\66"+
		"\2\2\u0169l\3\2\2\2\u016a\u016b\7*\2\2\u016bn\3\2\2\2\u016c\u016d\7+\2"+
		"\2\u016dp\3\2\2\2\u016e\u016f\7}\2\2\u016fr\3\2\2\2\u0170\u0171\7\177"+
		"\2\2\u0171t\3\2\2\2\u0172\u0173\7.\2\2\u0173v\3\2\2\2\u0174\u0175\7<\2"+
		"\2\u0175x\3\2\2\2\u0176\u0177\7=\2\2\u0177z\3\2\2\2\u0178\u0179\7?\2\2"+
		"\u0179\u017a\7@\2\2\u017a|\3\2\2\2\u017b\u017c\7,\2\2\u017c~\3\2\2\2\u017d"+
		"\u017e\7\61\2\2\u017e\u0080\3\2\2\2\u017f\u0180\7-\2\2\u0180\u0082\3\2"+
		"\2\2\u0181\u0182\7/\2\2\u0182\u0084\3\2\2\2\u0183\u0184\7?\2\2\u0184\u0086"+
		"\3\2\2\2\u0185\u0186\7/\2\2\u0186\u0187\7/\2\2\u0187\u0088\3\2\2\2\u0188"+
		"\u0189\7\u0080\2\2\u0189\u008a\3\2\2\2\u018a\u018b\7>\2\2\u018b\u008c"+
		"\3\2\2\2\u018c\u018d\7>\2\2\u018d\u018e\7?\2\2\u018e\u008e\3\2\2\2\u018f"+
		"\u0190\7>\2\2\u0190\u0191\7/\2\2\u0191\u0090\3\2\2\2\u0192\u0193\7B\2"+
		"\2\u0193\u0092\3\2\2\2\f\2\u012a\u0131\u0137\u0140\u0143\u0145\u0150\u015e"+
		"\u0166\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}