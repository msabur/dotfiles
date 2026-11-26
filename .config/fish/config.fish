if status is-interactive
    # Commands to run in interactive sessions can go here
    fish_add_path ~/.local/bin
    command -q zoxide && zoxide init fish | source
    set -g fish_greeting
    set -gx EDITOR /usr/bin/nvim
end
