cpp_token *
_cpp_lex_direct(cpp_reader *pfile)
{
    cppchar_t c;
    cpp_buffer *buffer;
    const unsigned char *comment_start;
    bool fallthrough_comment = false;
    cpp_token *result = pfile->cur_token++;

fresh_line:
    result->flags = 0;
    buffer = pfile->buffer;
    if (buffer->need_line)
    {
        if (pfile->state.in_deferred_pragma)
        {
            /* This can happen in cases like:
                #define loop(x) whatever
                #pragma omp loop
                where when trying to expand loop we need to peek
                next token after loop, but aren't still in_deferred_pragma
                mode but are in in_directive mode, so buffer->need_line
                is set, a CPP_EOF is peeked.  */
            result->type = CPP_PRAGMA_EOL;
            pfile->state.in_deferred_pragma = false;
            if (!pfile->state.pragma_allow_expansion)
                pfile->state.prevent_expansion--;
            return result;
        }
        if (!_cpp_get_fresh_line(pfile))
        {
            result->type = CPP_EOF;
            /* Not a real EOF in a directive or arg parsing -- we refuse
                to advance to the next file now, and will once we're out
                of those modes.  */
            if (!pfile->state.in_directive && !pfile->state.parsing_args)
            {
                /* Tell the compiler the line number of the EOF token.  */
                result->src_loc = pfile->line_table->highest_line;
                result->flags = BOL;
                /* Now pop the buffer that _cpp_get_fresh_line did not.  */
                _cpp_pop_buffer(pfile);
            }
            return result;
        }
        if (buffer != pfile->buffer)
            fallthrough_comment = false;
        if (!pfile->keep_tokens)
        {
            pfile->cur_run = &pfile->base_run;
            result = pfile->base_run.base;
            pfile->cur_token = result + 1;
        }
        result->flags = BOL;
        if (pfile->state.parsing_args == 2)
            result->flags |= PREV_WHITE;
    }
    buffer = pfile->buffer;
update_tokens_line:
    result->src_loc = pfile->line_table->highest_line;

skipped_white:
    if (buffer->cur >= buffer->notes[buffer->cur_note].pos && !pfile->overlaid_buffer)
    {
        _cpp_process_line_notes(pfile, false);
        result->src_loc = pfile->line_table->highest_line;
    }
    c = *buffer->cur++;
    // cannot print here, it will affect the .cc file that auto generated.
    // printf("%s:%s:%d:%d\n", __FILE__, __FUNCTION__, __LINE__, c);

    if (pfile->forced_token_location)
        result->src_loc = pfile->forced_token_location;
    else
        result->src_loc = linemap_position_for_column(pfile->line_table,
                                                      CPP_BUF_COLUMN(buffer, buffer->cur));
    // here lexing the token type
    switch (c)
    {
    case ' ':
    case '\t':
    case '\f':
    case '\v':
    case '\0':
        result->flags |= PREV_WHITE;
        skip_whitespace(pfile, c);
        goto skipped_white;

    case '\n':
        /* Increment the line, unless this is the last line ...  */
        if (buffer->cur < buffer->rlimit
            /* ... or this is a #include, (where _cpp_stack_file needs to
                unwind by one line) ...  */
            || (pfile->state.in_directive > 1
                /* ... except traditional-cpp increments this elsewhere.  */
                && !CPP_OPTION(pfile, traditional)))
            CPP_INCREMENT_LINE(pfile, 0);
        buffer->need_line = true;
        if (pfile->state.in_deferred_pragma)
        {
            /* Produce the PRAGMA_EOL on this line.  File reading
                ensures there is always a \n at end of the buffer, thus
                in a deferred pragma we always see CPP_PRAGMA_EOL before
                any CPP_EOF.  */
            result->type = CPP_PRAGMA_EOL;
            result->flags &= ~PREV_WHITE;
            pfile->state.in_deferred_pragma = false;
            if (!pfile->state.pragma_allow_expansion)
                pfile->state.prevent_expansion--;
            return result;
        }
        goto fresh_line;

    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
    {
        struct normalize_state nst = INITIAL_NORMALIZE_STATE;
        result->type = CPP_NUMBER;
        lex_number(pfile, &result->val.str, &nst);
        warn_about_normalization(pfile, result, &nst, false);
        break;
    }

    case 'L':
    case 'u':
    case 'U':
    case 'R':
        /* 'L', 'u', 'U', 'u8' or 'R' may introduce wide characters,
        wide strings or raw strings.  */
        if (c == 'L' || CPP_OPTION(pfile, rliterals) || (c != 'R' && CPP_OPTION(pfile, uliterals)))
        {
            if ((*buffer->cur == '\'' && c != 'R') || *buffer->cur == '"' || (*buffer->cur == 'R' && c != 'R' && buffer->cur[1] == '"' && CPP_OPTION(pfile, rliterals)) || (*buffer->cur == '8' && c == 'u' && ((buffer->cur[1] == '"' || (buffer->cur[1] == '\'' && CPP_OPTION(pfile, utf8_char_literals))) || (buffer->cur[1] == 'R' && buffer->cur[2] == '"' && CPP_OPTION(pfile, rliterals)))))
            {
                lex_string(pfile, result, buffer->cur - 1);
                break;
            }
        }
        /* Fall through.  */
        // this is where it determines the token type
    case '_':
    case 'a':
    case 'b':
    case 'c':
    case 'd':
    case 'e':
    case 'f':
    case 'g':
    case 'h':
    case 'i':
    case 'j':
    case 'k':
    case 'l':
    case 'm':
    case 'n':
    case 'o':
    case 'p':
    case 'q':
    case 'r':
    case 's':
    case 't':
    case 'v':
    case 'w':
    case 'x':
    case 'y':
    case 'z':
    case 'A':
    case 'B':
    case 'C':
    case 'D':
    case 'E':
    case 'F':
    case 'G':
    case 'H':
    case 'I':
    case 'J':
    case 'K':
    case 'M':
    case 'N':
    case 'O':
    case 'P':
    case 'Q':
    case 'S':
    case 'T':
    case 'V':
    case 'W':
    case 'X':
    case 'Y':
    case 'Z':
        result->type = CPP_NAME;
        {
            struct normalize_state nst = INITIAL_NORMALIZE_STATE;
            result->val.node.node = lex_identifier(pfile, buffer->cur - 1, false,
                                                   &nst,
                                                   &result->val.node.spelling);
            warn_about_normalization(pfile, result, &nst, true);
        }

        /* Convert named operators to their proper types.  */
        if (result->val.node.node->flags & NODE_OPERATOR)
        {
            result->flags |= NAMED_OP;
            result->type = (enum cpp_ttype)result->val.node.node->directive_index;
        }

        /* Signal FALLTHROUGH comment followed by another token.  */
        if (fallthrough_comment)
            result->flags |= PREV_FALLTHROUGH;
        break;

    case '\'':
    case '"':
        lex_string(pfile, result, buffer->cur - 1);
        break;

    case '/':
        /* A potential block or line comment.  */
        comment_start = buffer->cur;
        c = *buffer->cur;

        if (c == '*')
        {
            if (_cpp_skip_block_comment(pfile))
                cpp_error(pfile, CPP_DL_ERROR, "unterminated comment");
        }
        else if (c == '/' && !CPP_OPTION(pfile, traditional))
        {
            /* Don't warn for system headers.  */
            if (_cpp_in_system_header(pfile))
                ;
            /* Warn about comments if pedantically GNUC89, and not
                in system headers.  */
            else if (CPP_OPTION(pfile, lang) == CLK_GNUC89 && CPP_PEDANTIC(pfile) && !buffer->warned_cplusplus_comments)
            {
                if (cpp_error(pfile, CPP_DL_PEDWARN,
                              "C++ style comments are not allowed in ISO C90"))
                    cpp_error(pfile, CPP_DL_NOTE,
                              "(this will be reported only once per input file)");
                buffer->warned_cplusplus_comments = 1;
            }
            /* Or if specifically desired via -Wc90-c99-compat.  */
            else if (CPP_OPTION(pfile, cpp_warn_c90_c99_compat) > 0 && !CPP_OPTION(pfile, cplusplus) && !buffer->warned_cplusplus_comments)
            {
                if (cpp_error(pfile, CPP_DL_WARNING,
                              "C++ style comments are incompatible with C90"))
                    cpp_error(pfile, CPP_DL_NOTE,
                              "(this will be reported only once per input file)");
                buffer->warned_cplusplus_comments = 1;
            }
            /* In C89/C94, C++ style comments are forbidden.  */
            else if ((CPP_OPTION(pfile, lang) == CLK_STDC89 || CPP_OPTION(pfile, lang) == CLK_STDC94))
            {
                /* But don't be confused about valid code such as
                    - // immediately followed by *,
                - // in a preprocessing directive,
                - // in an #if 0 block.  */
                if (buffer->cur[1] == '*' || pfile->state.in_directive || pfile->state.skipping)
                {
                    result->type = CPP_DIV;
                    break;
                }
                else if (!buffer->warned_cplusplus_comments)
                {
                    if (cpp_error(pfile, CPP_DL_ERROR,
                                  "C++ style comments are not allowed in "
                                  "ISO C90"))
                        cpp_error(pfile, CPP_DL_NOTE,
                                  "(this will be reported only once per input "
                                  "file)");
                    buffer->warned_cplusplus_comments = 1;
                }
            }
            if (skip_line_comment(pfile) && CPP_OPTION(pfile, warn_comments))
                cpp_warning(pfile, CPP_W_COMMENTS, "multi-line comment");
        }
        else if (c == '=')
        {
            buffer->cur++;
            result->type = CPP_DIV_EQ;
            break;
        }
        else
        {
            result->type = CPP_DIV;
            break;
        }

        if (fallthrough_comment_p(pfile, comment_start))
            fallthrough_comment = true;

        if (pfile->cb.comment)
        {
            size_t len = pfile->buffer->cur - comment_start;
            pfile->cb.comment(pfile, result->src_loc, comment_start - 1,
                              len + 1);
        }

        if (!pfile->state.save_comments)
        {
            result->flags |= PREV_WHITE;
            goto update_tokens_line;
        }

        if (fallthrough_comment)
            result->flags |= PREV_FALLTHROUGH;

        /* Save the comment as a token in its own right.  */
        save_comment(pfile, result, comment_start, c);
        break;

    case '<':
        if (pfile->state.angled_headers)
        {
            lex_string(pfile, result, buffer->cur - 1);
            if (result->type != CPP_LESS)
                break;
        }

        result->type = CPP_LESS;
        if (*buffer->cur == '=')
        {
            buffer->cur++, result->type = CPP_LESS_EQ;
            if (*buffer->cur == '>' && CPP_OPTION(pfile, cplusplus) && CPP_OPTION(pfile, lang) >= CLK_GNUCXX20)
                buffer->cur++, result->type = CPP_SPACESHIP;
        }
        else if (*buffer->cur == '<')
        {
            buffer->cur++;
            IF_NEXT_IS('=', CPP_LSHIFT_EQ, CPP_LSHIFT);
        }
        else if (CPP_OPTION(pfile, digraphs))
        {
            if (*buffer->cur == ':')
            {
                /* C++11 [2.5/3 lex.pptoken], "Otherwise, if the next
                three characters are <:: and the subsequent character
                is neither : nor >, the < is treated as a preprocessor
                token by itself".  */
                if (CPP_OPTION(pfile, cplusplus) && CPP_OPTION(pfile, lang) != CLK_CXX98 && CPP_OPTION(pfile, lang) != CLK_GNUCXX && buffer->cur[1] == ':' && buffer->cur[2] != ':' && buffer->cur[2] != '>')
                    break;

                buffer->cur++;
                result->flags |= DIGRAPH;
                result->type = CPP_OPEN_SQUARE;
            }
            else if (*buffer->cur == '%')
            {
                buffer->cur++;
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
            buffer->cur++;
            IF_NEXT_IS('=', CPP_RSHIFT_EQ, CPP_RSHIFT);
        }
        break;

    case '%':
        result->type = CPP_MOD;
        if (*buffer->cur == '=')
            buffer->cur++, result->type = CPP_MOD_EQ;
        else if (CPP_OPTION(pfile, digraphs))
        {
            if (*buffer->cur == ':')
            {
                buffer->cur++;
                result->flags |= DIGRAPH;
                result->type = CPP_HASH;
                if (*buffer->cur == '%' && buffer->cur[1] == ':')
                    buffer->cur += 2, result->type = CPP_PASTE, result->val.token_no = 0;
            }
            else if (*buffer->cur == '>')
            {
                buffer->cur++;
                result->flags |= DIGRAPH;
                result->type = CPP_CLOSE_BRACE;
            }
        }
        break;

    case '.':
        result->type = CPP_DOT;
        if (ISDIGIT(*buffer->cur))
        {
            struct normalize_state nst = INITIAL_NORMALIZE_STATE;
            result->type = CPP_NUMBER;
            lex_number(pfile, &result->val.str, &nst);
            warn_about_normalization(pfile, result, &nst, false);
        }
        else if (*buffer->cur == '.' && buffer->cur[1] == '.')
            buffer->cur += 2, result->type = CPP_ELLIPSIS;
        else if (*buffer->cur == '*' && CPP_OPTION(pfile, cplusplus))
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
            buffer->cur++;
            result->type = CPP_DEREF;
            if (*buffer->cur == '*' && CPP_OPTION(pfile, cplusplus))
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
        if (*buffer->cur == ':' && CPP_OPTION(pfile, scope))
            buffer->cur++, result->type = CPP_SCOPE;
        else if (*buffer->cur == '>' && CPP_OPTION(pfile, digraphs))
        {
            buffer->cur++;
            result->flags |= DIGRAPH;
            result->type = CPP_CLOSE_SQUARE;
        }
        break;

    case '*':
        IF_NEXT_IS('=', CPP_MULT_EQ, CPP_MULT);
        break;
    case '=':
        IF_NEXT_IS('=', CPP_EQ_EQ, CPP_EQ);
        break;
    case '!':
        IF_NEXT_IS('=', CPP_NOT_EQ, CPP_NOT);
        break;
    case '^':
        IF_NEXT_IS('=', CPP_XOR_EQ, CPP_XOR);
        break;
    case '#':
        IF_NEXT_IS('#', CPP_PASTE, CPP_HASH);
        result->val.token_no = 0;
        break;

    case '?':
        result->type = CPP_QUERY;
        break;
    case '~':
        result->type = CPP_COMPL;
        break;
    case ',':
        result->type = CPP_COMMA;
        break;
    case '(':
        result->type = CPP_OPEN_PAREN;
        break;
    case ')':
        result->type = CPP_CLOSE_PAREN;
        break;
    case '[':
        result->type = CPP_OPEN_SQUARE;
        break;
    case ']':
        result->type = CPP_CLOSE_SQUARE;
        break;
    case '{':
        result->type = CPP_OPEN_BRACE;
        break;
    case '}':
        result->type = CPP_CLOSE_BRACE;
        break;
    case ';':
        result->type = CPP_SEMICOLON;
        break;

    /* @ is a punctuator in Objective-C.  */
    case '@':
        result->type = CPP_ATSIGN;
        break;

    default:
    {
        const uchar *base = --buffer->cur;
        static int no_warn_cnt;

        /* Check for an extended identifier ($ or UCN or UTF-8).  */
        struct normalize_state nst = INITIAL_NORMALIZE_STATE;
        if (forms_identifier_p(pfile, true, &nst))
        {
            result->type = CPP_NAME;
            result->val.node.node = lex_identifier(pfile, base, true, &nst,
                                                   &result->val.node.spelling);
            warn_about_normalization(pfile, result, &nst, true);
            break;
        }

        /* Otherwise this will form a CPP_OTHER token.  Parse valid UTF-8 as a
        single token.  */
        buffer->cur++;
        if (c >= utf8_signifier)
        {
            const uchar *pstr = base;
            cppchar_t s;
            if (_cpp_valid_utf8(pfile, &pstr, buffer->rlimit, 0, NULL, &s))
            {
                if (s > UCS_LIMIT && CPP_OPTION(pfile, cpp_warn_invalid_utf8))
                {
                    buffer->cur = base;
                    _cpp_warn_invalid_utf8(pfile);
                }
                buffer->cur = pstr;
            }
            else if (CPP_OPTION(pfile, cpp_warn_invalid_utf8))
            {
                buffer->cur = base;
                const uchar *end = _cpp_warn_invalid_utf8(pfile);
                buffer->cur = base + 1;
                no_warn_cnt = end - buffer->cur;
            }
        }
        else if (c >= utf8_continuation && CPP_OPTION(pfile, cpp_warn_invalid_utf8))
        {
            if (no_warn_cnt)
                --no_warn_cnt;
            else
            {
                buffer->cur = base;
                _cpp_warn_invalid_utf8(pfile);
                buffer->cur = base + 1;
            }
        }
        create_literal(pfile, result, base, buffer->cur - base, CPP_OTHER);
        break;
    }
    }

    /* Potentially convert the location of the token to a range.  */
    if (result->src_loc >= RESERVED_LOCATION_COUNT && result->type != CPP_EOF)
    {
        /* Ensure that any line notes are processed, so that we have the
        correct physical line/column for the end-point of the token even
        when a logical line is split via one or more backslashes.  */
        if (buffer->cur >= buffer->notes[buffer->cur_note].pos && !pfile->overlaid_buffer)
            _cpp_process_line_notes(pfile, false);

        source_range tok_range;
        tok_range.m_start = result->src_loc;
        tok_range.m_finish = linemap_position_for_column(pfile->line_table,
                                                         CPP_BUF_COLUMN(buffer, buffer->cur));

        result->src_loc = COMBINE_LOCATION_DATA(pfile->line_table,
                                                result->src_loc,
                                                tok_range, NULL, 0);
    }

    return result;
}