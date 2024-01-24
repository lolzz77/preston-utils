cpp_token * _cpp_lex_direct (cpp_reader *pfile)
{
	switch (c)
    {
		case ' ': case '\t': case '\f': case '\v': case '\0':
			result->flags |= PREV_WHITE;
			skip_whitespace (pfile, c);
				break;

		case '\n':
			break;

		case '0': case '1': case '2': case '3': case '4':
		case '5': case '6': case '7': case '8': case '9':
			result->type = CPP_NUMBER;
			break;

		case 'L':
		case 'u':
		case 'U':
		case 'R':
			break;

		case '_':
		case 'a': case 'b': case 'c': case 'd': case 'e': case 'f':
		case 'g': case 'h': case 'i': case 'j': case 'k': case 'l':
		case 'm': case 'n': case 'o': case 'p': case 'q': case 'r':
		case 's': case 't':           case 'v': case 'w': case 'x':
		case 'y': case 'z':
		case 'A': case 'B': case 'C': case 'D': case 'E': case 'F':
		case 'G': case 'H': case 'I': case 'J': case 'K':
		case 'M': case 'N': case 'O': case 'P': case 'Q':
		case 'S': case 'T':           case 'V': case 'W': case 'X':
		case 'Y': case 'Z':
			result->type = CPP_NAME;
			result->flags |= NAMED_OP;
			break;

		case '\'':
		case '"':
			break;

		case '/':
			if (c == '*')
			{
				result->type = CPP_MULTILINE_COMMENT;
			}
			else if (c == '/')
			{
				result->type = CPP_SINGLE_LINE_COMMENT;
			}
			else if (c == '=')
			{
				result->type = CPP_DIV_EQ;
				break;
			}
			else
			{
				result->type = CPP_DIV;
				break;
			}
			break;

		case '<':
			result->type = CPP_LESS;
			if (*buffer->cur == '=')
			{
				buffer->cur++, result->type = CPP_LESS_EQ;
				if (*buffer->cur == '>')
				{
					buffer->cur++, result->type = CPP_SPACESHIP;
				}
			}
			else if (*buffer->cur == '<')
			{
				IF_NEXT_IS ('=', CPP_LSHIFT_EQ, CPP_LSHIFT);
			}
			else if (CPP_OPTION (pfile, digraphs))
			{
				if (*buffer->cur == ':')
				{
					result->flags |= DIGRAPH;
					result->type = CPP_OPEN_SQUARE;
				}
				else if (*buffer->cur == '%')
				{
					result->flags |= DIGRAPH;
					result->type = CPP_OPEN_BRACE;
				}
			}
			break;

		case '>':
			result->type = CPP_GREATER;
			if (*buffer->cur == '=')
				buffer->cur++, result->type = CPP_GREATER_EQ;
			else if (*buffer->cur == '>')
			{
				IF_NEXT_IS ('=', CPP_RSHIFT_EQ, CPP_RSHIFT);
			}
			break;

		case '%':
			result->type = CPP_MOD;
			if (*buffer->cur == '=')
				buffer->cur++, result->type = CPP_MOD_EQ;
			else if (CPP_OPTION (pfile, digraphs))
			{
				if (*buffer->cur == ':')
				{
					result->flags |= DIGRAPH;
					result->type = CPP_HASH;
					if (*buffer->cur == '%' && buffer->cur[1] == ':')
						buffer->cur += 2, result->type = CPP_PASTE, result->val.token_no = 0;
				}
				else if (*buffer->cur == '>')
				{
					result->flags |= DIGRAPH;
					result->type = CPP_CLOSE_BRACE;
				}
			}
			break;

		case '.':
			result->type = CPP_DOT;
			if (ISDIGIT (*buffer->cur))
			{
				struct normalize_state nst = INITIAL_NORMALIZE_STATE;
				result->type = CPP_NUMBER;
				lex_number (pfile, &result->val.str, &nst);
				warn_about_normalization (pfile, result, &nst, false);
			}
			else if (*buffer->cur == '.' && buffer->cur[1] == '.')
				buffer->cur += 2, result->type = CPP_ELLIPSIS;
			else if (*buffer->cur == '*' && CPP_OPTION (pfile, cplusplus))
				buffer->cur++, result->type = CPP_DOT_STAR;
			break;

		case '+':
			result->type = CPP_PLUS;
			if (*buffer->cur == '+')
				buffer->cur++, result->type = CPP_PLUS_PLUS;
			else if (*buffer->cur == '=')
				buffer->cur++, result->type = CPP_PLUS_EQ;
			break;

		case '-':
			result->type = CPP_MINUS;
			if (*buffer->cur == '>')
			{
				result->type = CPP_DEREF;
				if (*buffer->cur == '*' && CPP_OPTION (pfile, cplusplus))
					buffer->cur++, result->type = CPP_DEREF_STAR;
			}
			else if (*buffer->cur == '-')
				buffer->cur++, result->type = CPP_MINUS_MINUS;
			else if (*buffer->cur == '=')
				buffer->cur++, result->type = CPP_MINUS_EQ;
			break;

		case '&':
			result->type = CPP_AND;
			if (*buffer->cur == '&')
				buffer->cur++, result->type = CPP_AND_AND;
			else if (*buffer->cur == '=')
				buffer->cur++, result->type = CPP_AND_EQ;
			break;

		case '|':
			result->type = CPP_OR;
			if (*buffer->cur == '|')
				buffer->cur++, result->type = CPP_OR_OR;
			else if (*buffer->cur == '=')
				buffer->cur++, result->type = CPP_OR_EQ;
			break;

		case ':':
			result->type = CPP_COLON;
			if (*buffer->cur == ':' && CPP_OPTION (pfile, scope))
				buffer->cur++, result->type = CPP_SCOPE;
			else if (*buffer->cur == '>' && CPP_OPTION (pfile, digraphs))
			{
				result->flags |= DIGRAPH;
				result->type = CPP_CLOSE_SQUARE;
			}
			break;

		case '*': IF_NEXT_IS ('=', CPP_MULT_EQ, CPP_MULT); break;
		case '=': IF_NEXT_IS ('=', CPP_EQ_EQ, CPP_EQ); break;
		case '!': IF_NEXT_IS ('=', CPP_NOT_EQ, CPP_NOT); break;
		case '^': IF_NEXT_IS ('=', CPP_XOR_EQ, CPP_XOR); break;
		case '#': IF_NEXT_IS ('#', CPP_PASTE, CPP_HASH); result->val.token_no = 0; break;

		case '?': result->type = CPP_QUERY; break;
		case '~': result->type = CPP_COMPL; break;
		case ',': result->type = CPP_COMMA; break;
		case '(': result->type = CPP_OPEN_PAREN; break;
		case ')': result->type = CPP_CLOSE_PAREN; break;
		case '[': result->type = CPP_OPEN_SQUARE; break;
		case ']': result->type = CPP_CLOSE_SQUARE; break;
		case '{': result->type = CPP_OPEN_BRACE; break;
		case '}': result->type = CPP_CLOSE_BRACE; break;
		case ';': result->type = CPP_SEMICOLON; break;


		default:
			{
				/* Check for an extended identifier ($ or UCN or UTF-8).  */
				struct normalize_state nst = INITIAL_NORMALIZE_STATE;
				if (forms_identifier_p (pfile, true, &nst))
				{
					result->type = CPP_NAME;
					result->val.node.node = lex_identifier (pfile, base, true, &nst,
															&result->val.node.spelling);
					break;
				}
				create_literal (pfile, result, base, buffer->cur - base, CPP_OTHER);
				break;
			}

    }


  return result;
}