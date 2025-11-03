function mkcd -d 'Make a directory then cd into it'
    mkdir -p "$argv"
    cd "$argv"
end

alias open=xdg-open
alias vim=nvim
alias tb="nc termbin.com 9999"

