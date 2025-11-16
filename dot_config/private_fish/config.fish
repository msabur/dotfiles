if status is-interactive
    # Commands to run in interactive sessions can go here
    fish_add_path ~/.local/bin
    command -q pyenv && pyenv init - fish | source
    command -q zoxide && zoxide init fish | source
    set -g fish_greeting
end
