const fs = require('fs');
const path = require('path');
const vsctm = require('vscode-textmate');
const oniguruma = require('vscode-oniguruma');
const readline = require('readline');

// is best to initialize it with some value
const param = ['source.c', './allFunc.c'];

// Param to control what test you wanna do
// const param = ['source.c', './test/mytest/test5.c'];
// const param = ['source.c', './test/mytest/test2.c'];
// const param = ['source.cpp', './test/mytest/test7.cpp'];


/***
 * process.argv is an array
 * 
 * index 0 = /usr/bin/node
 * index 1 = this script file name
 * index 2 = any extra arugment u passed from command
 * eg: node [this scritp file name] [hello]
 * index 2 = hello
 */
full_path = process.argv[2]
file_exntension = full_path.substring(full_path.lastIndexOf('.') + 1);
if(file_exntension == 'c')
    param[0] = 'source.c'
else if(file_exntension == 'cpp' || file_exntension == 'cc')
    param[0] = 'source.cpp'
param[1] = full_path

/**
 * Utility to read a file as a promise
 */
function readFile(path) {
    return new Promise((resolve, reject) => {
        fs.readFile(path, (error, data) => error ? reject(error) : resolve(data));
    })
}

const wasmBin = fs.readFileSync(path.join(__dirname, './node_modules/vscode-oniguruma/release/onig.wasm')).buffer;
const vscodeOnigurumaLib = oniguruma.loadWASM(wasmBin).then(() => {
    return {
        createOnigScanner(patterns) { return new oniguruma.OnigScanner(patterns); },
        createOnigString(s) { return new oniguruma.OnigString(s); }
    };
});

// Create a registry that can create a grammar from a scope name.
const registry = new vsctm.Registry({
    onigLib: vscodeOnigurumaLib,
    loadGrammar: (scopeName) => {
        if (scopeName === 'source.c') {
            // https://github.com/textmate/javascript.tmbundle/blob/master/Syntaxes/JavaScript.plist
            return readFile(path.join(__dirname, './jsonFile/c.tmLanguage.json')).then((data) => vsctm.parseRawGrammar(data.toString(), path.join(__dirname, './../jsonFile/c.tmLanguage.json')))
        }
        if (scopeName === 'source.cpp') {
            // https://github.com/textmate/javascript.tmbundle/blob/master/Syntaxes/JavaScript.plist
            return readFile(path.join(__dirname, './jsonFile/cpp.tmLanguage.json')).then((data) => vsctm.parseRawGrammar(data.toString(), path.join(__dirname, './../jsonFile/c.tmLanguage.json')))
        }
        // console.log(`Unknown scope name: ${scopeName}`);
        return null;
    }
});


/* Definition scopes for C
*
* Function definition
* source.c, meta.function.c, meta.function.definition.parameters.c, entity.name.function.c
* source.cpp, entity.name.function.call.cpp
* 
* Function call
* source.c, meta.block.c, meta.function-call.c, entity.name.function.c
* 
* Parenthesis/round bracket
* source.c, meta.function.c, meta.function.definition.parameters.c, punctuation.section.parameters.begin.bracket.round.c
* source.c, meta.function.c, meta.function.definition.parameters.c, punctuation.section.parameters.end.bracket.round.c
* 
* Curly bracket
* source.c, meta.block.c, punctuation.section.block.begin.bracket.curly.c
* source.c, meta.block.c, punctuation.section.block.end.bracket.curly.c
* 
* Terminator
* source.c, meta.block.c, punctuation.terminator.statement.c
*/ 

/* Definition scopes for CPP
*
* Function definition (not class)
* source.cpp, meta.function.definition.cpp, meta.head.function.definition.cpp, entity.name.function.definition.cpp
* Conclusion: better use (entity.name.function.definition.cpp) to detect this one
* 
* Class function definition outside of class (format: void class::function()) (some got multiple scopes)
* (class)       -> source.cpp, entity.name.scope-resolution.cpp
* (class)       -> source.cpp, entity.name.scope-resolution.function.call.cpp
* (::)          -> source.cpp, punctuation.separator.namespace.access.cpp, punctuation.separator.scope-resolution.cpp
* (::)          -> source.cpp, punctuation.separator.namespace.access.cpp, punctuation.separator.scope-resolution.function.call.cpp
* (function())  -> source.cpp, entity.name.function.call.cpp
* (function())  -> source.cpp, entity.name.function.call.cpp
* Conclusion: better use (class) to detect this one
* 
* Class function definition inside of class
* source.cpp, meta.block.class.cpp, meta.body.class.cpp, meta.function.definition.cpp, meta.head.function.definition.cpp, entity.name.function.definition.cpp
* Conclusion: better use (entity.name.function.definition.cpp) to detect this one
* 
* Function call
* source.cpp, meta.function.definition.cpp, meta.body.function.definition.cpp, entity.name.function.call.cpp
* source.cpp, meta.function.definition.cpp, meta.body.function.definition.cpp, entity.name.function.call.cpp, meta.block.cpp
* 
* Parenthesis/round bracket
* source.cpp, meta.block.class.cpp, meta.body.class.cpp, meta.function.definition.cpp, meta.head.function.definition.cpp, punctuation.section.parameters.begin.bracket.round.cpp (this is function definition inside of class)
* source.cpp, punctuation.section.arguments.begin.bracket.round.function.call.cpp (this is for cases that define class definition outside of class)
* source.cpp, meta.function.definition.cpp, meta.head.function.definition.cpp, punctuation.section.parameters.begin.bracket.round.cpp (this is normal function defnition)
* source.cpp, punctuation.section.arguments.begin.bracket.round.function.call.cpp

* Curly bracket (enum, struct, class, all diff scope names) (replace 'begin' to 'end' urself)
* source.cpp, meta.block.cpp, punctuation.section.block.begin.bracket.curly.cpp (this is if else curly bracket)
* source.cpp, meta.function.definition.cpp, meta.body.function.definition.cpp, meta.block.cpp, meta.block.cpp, punctuation.section.block.begin.bracket.curly.cpp (this is if else curly bracket)
* source.cpp, meta.function.definition.cpp, meta.body.function.definition.cpp, meta.block.switch.cpp, meta.body.switch.cpp, meta.block.cpp, punctuation.section.block.begin.bracket.curly.cpp (this is 'case' curly bracket)
* source.cpp, meta.block.class.cpp, meta.head.class.cpp, punctuation.section.block.begin.bracket.curly.class.cpp (this is class curly bracket)
* source.cpp, meta.function.definition.cpp, meta.head.function.definition.cpp, punctuation.section.block.begin.bracket.curly.function.definition.cpp
* source.cpp, meta.block.class.cpp, meta.body.class.cpp, meta.function.definition.cpp, meta.head.function.definition.cpp, punctuation.section.block.begin.bracket.curly.function.definition.cpp

* Terminator
* source.cpp, meta.function.definition.cpp, meta.body.function.definition.cpp, punctuation.terminator.statement.cpp
*/ 


// Load the JavaScript grammar and any other grammars included by it async.
registry.loadGrammar(param[0]).then(grammar => {
    let lines = [];

    // Read file that you want to tokenize
    // Separate them by newline, and push into list
    const fileStream = fs.createReadStream(path.join('', param[1]));

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });
    
    rl.on('line', (line) => {
        // push each line into list
        lines.push(line);
    });
    
    // tokenize line
    rl.on('close', () => {
        let ruleStack = vsctm.INITIAL;

        /*** 
         *  -1 is because the checking to put log into function
         * is check value==0 one
         * there may be cases that, the value did not get incremented at all
         * that is, if i initialize it to 0,
         * Then the checking will treat this as valid
         * For function, round bracket is 100% will have
         * So, i need it to tell me whether round backets have been detected or not
         * If no, means it is not a function definition
         */ 
        let curly_bracket_count = -1;
        let round_bracket_count = -1;
        let pending_is_prototype_or_function = false;
        let is_inline = false; // functino that has 'inline' keyword, cannot put log
        let setup_parameters = false;
        let is_function_definition = false; // to tell is the line currently in function body
        let skip = false;
        
        /**
         * Whenever a function name is detected
         * Need to verify is prototype or not
         * Because textmate uses line-by-line approach
         * Thus, use this to hold the values first
         */
        let prev_token_start_index = 0;
        let prev_token_end_index = 0;
        let prev_token_scopes = '';
        let prev_token_line = 0;
        let prev_token_line_substr = '';

        /***
         * For caller option: (havent implement yet)
         * Dont match
         * 1. prototype
         * 2. Caller in an inline function
         */

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const lineTokens = grammar.tokenizeLine(line, ruleStack);
            let string_to_check = ''
            // console.log(`\nTokenizing line: ${line}`);
            for (let j = 0; j < lineTokens.tokens.length; j++) {
                const token = lineTokens.tokens[j];
                // this token_str_debug is for debugging purposes, where u can add into watch n see what string
                let token_str_debug = line.substring(token.startIndex, token.endIndex);
                if (token_str_debug == 'c_parser_require')
                {
                    let x = 1
                }


                if (param[0] == 'source.c')
                {
                    /***
                     * Function definition for C
                     */
                    function_1_scopes = [
                        'meta.function.c',
                        'meta.function.definition.parameters.c',
                        'entity.name.function.c'
                    ]

                    /****
                     * Comments, 
                     * strings in single/double quote
                     * skip these, if not they will mess up with
                     * () {} bracket counting
                     */
                    skip_1_scopes = [
                        'comment.block.c',
                        'comment.line.double-slash.c',
                        'string.quoted.single.c',
                        'string.quoted.double.c'
                    ]
                    
                    if (
                        function_1_scopes.every(scope => token.scopes.includes(scope))
                    ) {
                        setup_parameters = true;
                    }

                    if (
                        skip_1_scopes.some(scope => token.scopes.includes(scope))
                    ) {
                        skip = true;
                    }
                }
                else if (param[0] == 'source.cpp')
                {
                    /***
                     * Function definition, 
                     * either class one that defined outside of class
                     * or non class
                    */
                    function_1_scopes = [
                        'meta.function.definition.cpp',
                        'meta.head.function.definition.cpp',
                        'entity.name.function.definition.cpp'
                    ]
                    /**
                     * Function definition,
                     * Class's one
                     * Defined inside the class
                     */
                    function_2_scopes = [
                        'entity.name.scope-resolution.cpp'
                    ]
                    /**
                     * Function definition,
                     * Class's one
                     * Defined outside the class
                     */
                    function_3_scopes = [
                        'entity.name.scope-resolution.function.call.cpp'
                    ]

                    /****
                     * Comments, 
                     * strings in single/double quote
                     */
                    skip_1_scopes = [
                        'comment.block.cpp',
                        'comment.line.double-slash.cpp',
                        'string.quoted.double.cpp',
                        'string.quoted.single.cpp',
                    ]

                    if (
                        function_1_scopes.every(scope => token.scopes.includes(scope))||
                        function_2_scopes.every(scope => token.scopes.includes(scope))||
                        function_3_scopes.every(scope => token.scopes.includes(scope))
                    ) {
                        setup_parameters = true;
                    }

                    if (
                        skip_1_scopes.some(scope => token.scopes.includes(scope))
                    ) {
                        skip = true;
                    }
                }

                if(skip)
                {
                    skip = false;
                    continue;
                }

                if(setup_parameters)
                {
                    pending_is_prototype_or_function = true;
                    prev_token_start_index = token.startIndex;
                    prev_token_end_index = token.endIndex;
                    prev_token_scopes = token.scopes.join(', ');
                    prev_token_line = i+1;
                    prev_token_line_substr = line.substring(token.startIndex, token.endIndex);

                    setup_parameters = false;
                }

                // this is inline function, cannot add log in it
                if(
                    line.substring(token.startIndex, token.endIndex)=='inline'
                )
                {
                    is_inline = true;
                }
                if(pending_is_prototype_or_function)
                {
                    // this is not function definition, end it
                    if(
                        (line.substring(token.startIndex, token.endIndex)==';') &&
                        (is_function_definition==false)
                    )
                    {
                        pending_is_prototype_or_function = false;
                        is_inline = false;
                        round_bracket_count = -1;
                        curly_bracket_count = -1;
                        break;
                    }

                    // function definition parenthesis
                    if(
                        line.substring(token.startIndex, token.endIndex)=='('
                    )
                    {
                        if(round_bracket_count==-1)
                            round_bracket_count=0;
                        round_bracket_count++;
                    }
                    else if(
                        line.substring(token.startIndex, token.endIndex)==')'
                    )
                    {
                        round_bracket_count--;
                    }

                    // this might be curly bracket in the paranthesis
                    // or also the function opening bracket
                    if(
                        line.substring(token.startIndex, token.endIndex)=='{'
                    )
                    {
                        if(curly_bracket_count==-1)
                            curly_bracket_count=0;
                        curly_bracket_count++;
                    }
                    else if(
                        line.substring(token.startIndex, token.endIndex)=='}'
                    )
                    {
                        curly_bracket_count--
                    }

                    // this closing bracket is the function closing bracket
                    if(
                        (line.substring(token.startIndex, token.endIndex)=='}') &&
                        (curly_bracket_count==0) &&
                        (round_bracket_count==0)
                    )
                    {
                        pending_is_prototype_or_function = false;
                        is_function_definition = false;
                        round_bracket_count = -1;
                        curly_bracket_count = -1;
                        
                        // to ensure that it doesnt print closing bracket of an inline function
                        if(is_inline==false)
                            // Print the closing bracket
                            print_onto_console(i+1, token.startIndex, token.endIndex, line.substring(token.startIndex, token.endIndex), token.scopes.join(', '), false);
                        
                        is_inline = false;
                    }

                    // is function definition
                    if(
                        (line.substring(token.startIndex, token.endIndex)=='{')&&
                        (round_bracket_count==0)&&
                        (curly_bracket_count==1)&&
                        (is_inline==false)
                    )
                    {
                        is_function_definition = true;

                        // Print the function name
                        print_onto_console(prev_token_line, prev_token_start_index, prev_token_end_index, prev_token_line_substr, prev_token_scopes, false);
                        
                        // Print the opening bracket
                        print_onto_console(i+1, token.startIndex, token.endIndex, line.substring(token.startIndex, token.endIndex), token.scopes.join(', '), true);
                    }
                }
                
                

                // Debug: exchange comment/uncomment this line if want to enable loop
                for(let z = 0; z < 0; z ++)
                // for(let z = 0; z < token.scopes.length + 1; z ++)
                {
                    /******************************************
                     * Original functino to print all tokens
                     **************************************************/
                    const token = lineTokens.tokens[j];
                    console.log(`Line ${i+1} - token from ${token.startIndex} to ${token.endIndex} ` +
                        `(${line.substring(token.startIndex, token.endIndex)}) ` +
                        `with scopes ${token.scopes.join(', ')}`
                    );

                    /***************************************************************
                    * this is to check the line, what scopes are they
                    ****************************************************************/
                    if(line.includes(string_to_check))
                    {
                        console.log(`line ${i+1} - token from ${token.startIndex} to ${token.endIndex} ` +
                                    `(${line.substring(token.startIndex, token.endIndex)}) ` +
                                    `with scopes ${token.scopes.join(', ')}`
                        )
                        break;
                    }
                }
            }
            ruleStack = lineTokens.ruleStack;
        }
    });
    
});

function print_onto_console(line_number, token_start_index, token_end_index, token_line_substr, token_scopes, to_print)
{
    // Debug: comment this out to print out those caller that passed in FALSE
    if(!to_print)
        return

    // console.log(`line ${line_number} - token from ${token_start_index} to ${token_end_index} ` +
    //             `(${token_line_substr}) ` +
    //             `with scopes ${token_scopes}`
    // );
    // console.log(`line ${line_number} : index ${token_start_index} : ${token_line_substr}`);
    console.log(`${line_number}:${token_start_index}`);
}

/* OUTPUT:

Unknown scope name: source.js.regexp

Tokenizing line: function sayHello(name) {
 - token from 0 to 8 (function) with scopes source.js, meta.function.js, storage.type.function.js
 - token from 8 to 9 ( ) with scopes source.js, meta.function.js
 - token from 9 to 17 (sayHello) with scopes source.js, meta.function.js, entity.name.function.js
 - token from 17 to 18 (() with scopes source.js, meta.function.js, punctuation.definition.parameters.begin.js
 - token from 18 to 22 (name) with scopes source.js, meta.function.js, variable.parameter.function.js
 - token from 22 to 23 ()) with scopes source.js, meta.function.js, punctuation.definition.parameters.end.js
 - token from 23 to 24 ( ) with scopes source.js
 - token from 24 to 25 ({) with scopes source.js, punctuation.section.scope.begin.js

Tokenizing line:        return "Hello, " + name;
 - token from 0 to 1 (  ) with scopes source.js
 - token from 1 to 7 (return) with scopes source.js, keyword.control.js
 - token from 7 to 8 ( ) with scopes source.js
 - token from 8 to 9 (") with scopes source.js, string.quoted.double.js, punctuation.definition.string.begin.js
 - token from 9 to 16 (Hello, ) with scopes source.js, string.quoted.double.js
 - token from 16 to 17 (") with scopes source.js, string.quoted.double.js, punctuation.definition.string.end.js
 - token from 17 to 18 ( ) with scopes source.js
 - token from 18 to 19 (+) with scopes source.js, keyword.operator.arithmetic.js
 - token from 19 to 20 ( ) with scopes source.js
 - token from 20 to 24 (name) with scopes source.js, support.constant.dom.js
 - token from 24 to 25 (;) with scopes source.js, punctuation.terminator.statement.js

Tokenizing line: }
 - token from 0 to 1 (}) with scopes source.js, punctuation.section.scope.end.js

*/