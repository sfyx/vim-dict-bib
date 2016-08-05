" vim-dict - The Dict client for Vim
" Maintainer:   Szymon Wrozynski
" Version:      1.2.1
"
" Installation:
" Place in ~/.vim/plugin/dict.vim or in case of Pathogen:
"
"     cd ~/.vim/bundle
"     git clone https://github.com/szw/vim-dict.git
"
" License:
" Copyright (c) 2012 Szymon Wrozynski. Distributed under the same terms as Vim itself.
" See :help license
"
" Usage:
" https://github.com/szw/vim-dict/blob/master/README.md
"

if exists("g:loaded_dict") || &cp || v:version < 700
    finish
endif

let g:loaded_dict = 1

if !exists("g:dict_curl_command")
    let g:dict_curl_command = "curl"
endif

if !exists("g:dict_curl_options")
    let g:dict_curl_options = "--connect-timeout 30"
endif

if !exists("g:dict_hosts")
    let g:dict_hosts = [["dict.org", ["all"]]]
endif

if !exists("g:dict_leave_pw")
    let g:dict_leave_pw = 0
endif

command! -nargs=? -range Dict :call s:dict(<q-args>)

command! -nargs=0 DictShowDb :call s:dict_show_db()

fun! s:dict(word)
    if (getpos('.') == getpos("'<")) && empty(a:word)
        let word = getline("'<")[getpos("'<")[2] - 1:getpos("'>")[2] - 1]
    else
        let word = empty(a:word) ? expand("<cword>") : a:word
    endif

    let word = substitute(tolower(word), '^\s*\(.\{-}\)\s*$', '\1', '')
    let quoted_word = "\"" . word . "\""

    silent! | redraw | echo "Performing lookup for" quoted_word "- please wait..."

    silent! exe "noautocmd botright pedit Dict:'" . word . "'"
    noautocmd wincmd P
    setlocal modifiable
    setlocal buftype=nofile ff=unix
    setlocal nobuflisted

    "for host in g:dict_hosts
    "    for db in host[1]
    "        silent! exe "noautocmd r!" g:dict_curl_command "-s" g:dict_curl_options "dict://" . host[0] . "/d:" . quoted_word . ":" . db
    "    endfor
    "endfor

    silent! exe escape("noautocmd r! curl -s 'http://cn.bing.com/dict/search?q=".join(split(word), "+")."&form=BDVSP6&mkt=zh-cn' | hxnormalize -x |hxremove '.sen_ime' | hxremove '.li_ex' | hxremove '.wd_div' | hxremove '.df_div .tb_div' | hxremove '.pos_lin' | hxremove '.pos1' | hxremove '.hw_ti' | hxremove '.sen_li' | hxremove '.web_area' |  hxselect '.lf_area' | hxremove '.filter' | hxremove '#filshow' | hxremove '#filhide' | hxremove 'img' | hxremove '.bi_pag' | hxremove '.gra' | hxremove '.dis' | hxremove '.infor' | hxremove '.dymp_link' | html2text -utf8 -width 150 -nobs ","#")

    silent! exe "%s/&quot;/\"/g"
    silent! exe "%s/\\([0-9][0-9]*.\\)\\n/\\1 /g"

    silent! exe "%s/^151 //g"
    silent! exe "%s/^153 //g"
    silent! exe "%s/^\.$/--------------------------------------------------------------------------------/g"
    silent! exe "g/^[0-9][0-9][0-9]/d_"
    silent! exe "1d_"

    if line("$") == 1
        silent! exe "normal! a Nothing found for" quoted_word
    endif

    setlocal nomodifiable
    setlocal nofoldenable
    nnoremap <buffer><silent> q :bw!<CR>

    if g:dict_leave_pw
        noautocmd wincmd p
    endif
endfun


fun! s:dict_show_db()
    silent! | redraw | echo "Connecting to DICT servers - please wait..."

    silent! exe "noautocmd botright pedit Dict:show:db"
    noautocmd wincmd P
    setlocal modifiable
    set buftype=nofile ff=unix
    setlocal nobuflisted

    for host in g:dict_hosts
        silent! exe "normal! I--------------------------------------------------------------------------------\r"
        silent! exe "normal! IServer: " . host[0] . "\r"
        silent! exe "normal! I--------------------------------------------------------------------------------\r"
        silent! exe "noautocmd r!" g:dict_curl_command "-s" g:dict_curl_options "dict://" . host[0] . "/show:db"
    endfor

    silent! exe "%s/^110 //g"
    silent! exe "%s/^\.$//g"
    silent! exe "g/^\s*[0-9][0-9][0-9]/d_"
    silent! exe "g/^$/d_"
    silent! exe "0"

    setlocal nomodifiable
    setlocal nofoldenable
    nnoremap <buffer><silent> q :bw!<CR>

    if g:dict_leave_pw
        noautocmd wincmd p
    endif
endfun


let s:path = expand('<sfile>:p:h')
command! -nargs=? -range Bibtex :call s:bibtex(<q-args>)
fun! s:bibtex(word)
    if (getpos('.') == getpos("'<")) && empty(a:word)
        let word = getline("'<")[getpos("'<")[2] - 1:getpos("'>")[2] - 1]
    else
        let word = empty(a:word) ? expand("<cword>") : a:word
    endif

    let word = substitute(tolower(word), '^\s*\(.\{-}\)\s*$', '\1', '')
    let quoted_word = "\"" . word . "\""

    silent! | redraw | echo "Performing bibtex lookup for" quoted_word "- please wait..."


    silent! exe "noautocmd botright pedit Bibtex"
    "silent! exe "noautocmd botright pedit Bibtex:'" . word . "'"
    noautocmd wincmd P
    setlocal modifiable
    setlocal buftype=nofile ff=unix
    setlocal nobuflisted

    "for host in g:dict_hosts
    "    for db in host[1]
    "        silent! exe "noautocmd r!" g:dict_curl_command "-s" g:dict_curl_options "dict://" . host[0] . "/d:" . quoted_word . ":" . db
    "    endfor
    "endfor

    silent! exe escape("noautocmd r! python ".s:path ."/ieee.py ".quoted_word,"#")

    silent! exe "%s///g"
    "silent! exe "%s/&quot;/\"/g"
    "silent! exe "%s/\\([0-9][0-9]*.\\)\\n/\\1 /g"

    "silent! exe "%s/^151 //g"
    "silent! exe "%s/^153 //g"
    "silent! exe "%s/^\.$/--------------------------------------------------------------------------------/g"
    "silent! exe "g/^[0-9][0-9][0-9]/d_"
    silent! exe "1d_"

    if line("$") == 1
        silent! exe "normal! a Nothing found for" quoted_word
    endif

    setlocal nomodifiable
    setlocal nofoldenable
    nnoremap <buffer><silent> q :bw!<CR>

    if g:dict_leave_pw
        noautocmd wincmd p
    endif
endfun

