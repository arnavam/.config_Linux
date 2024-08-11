#!/usr/bin/env bash

## Uncomment to disable git info
#powerline_git=0
[[ -f ~/.cache/wal/colors.sh ]] && . ~/.cache/wal/colors.sh
__powerline() {
    # Colors
    reset='\[\033[m\]'
    blue='\[\033[0;34m\]'
    cyan='\[\033[0;36m\]'
    green='\[\033[0;32m\]'
    red='\[\033[0;31m\]'
    purple='\[\033[0;35m\]'
    yellow='\[\033[0;33m\]'
    bright_green='\[\033[01;32m\]'
    bright_red='\[\033[01;31m\]'
    bright_blue='\[\033[01;34m\]'
    bright_yellow='\[\033[01;33m\]'
    gradient_green='\[\033[38;5;82m\]'
    gradient_light_green='\[\033[38;5;118m\]'
    # Symbols
    symbol_git_branch=${symbol_git_branch:-⑂ }
    symbol_git_modified=${symbol_git_modified:-*}
    symbol_git_push=${symbol_git_push:-↑}
    symbol_git_pull=${symbol_git_pull:-↓}

    __git_info() { 
        [[ $powerline_git = 0 ]] && return # disabled
        [[ -f .gitignore ]] && return # if .gitignore exists, return
        hash git 2>/dev/null || return # git not found
        local git_eng="env LANG=C git"   # force git output in English to make our work easier

        # get current branch name
        local ref=$($git_eng symbolic-ref --short HEAD 2>/dev/null)

        if [[ -n "$ref" ]]; then
            # prepend branch symbol
            ref=$symbol_git_branch$ref
        else
            # get tag name or short unique hash
            ref=$($git_eng describe --tags --always 2>/dev/null)
        fi

        [[ -n "$ref" ]] || return  # not a git repo

        local marks

        # scan first two lines of output from `git status`
        while IFS= read -r line; do
            if [[ $line =~ ^## ]]; then # header line
                [[ $line =~ ahead\ ([0-9]+) ]] && marks+=" $symbol_git_push${BASH_REMATCH[1]}"
                [[ $line =~ behind\ ([0-9]+) ]] && marks+=" $symbol_git_pull${BASH_REMATCH[1]}"
            else # branch is modified if output contains more lines after the header line
                marks="$symbol_git_modified$marks"
                break
            fi
        done < <($git_eng status --porcelain --branch 2>/dev/null)  # note the space between the two <

        # print the git branch segment without a trailing newline
        printf " $ref$marks"
    }

    ps1() {
        # Check the exit code of the previous command and display different
        # colors in the prompt accordingly. 
        if [ $? -eq 0 ]; then
            local symbol="$green\$ $reset"
        else
            local symbol="$red\$ $reset"
        fi

        local user_host="${cyan}\u@\h${reset}"
        if [[ "$PWD" == "/" ]]; then
            cwd="${bright_red}λ${reset}"  # Red for root directory
        elif [[ "$PWD" == "$HOME" ]]; then
            cwd="${bright_blue} 󰋞${reset}"  # Blue with house icon for home
        else
            cwd="${bright_blue}\w${reset}"
        fi
        local jobs_count="\[\033[01;31m\]$(jobs | wc -l) jobs\[\033[00m\]"  # Red for job count
        local datetime="${bright_yellow}\D{%F %T}${reset}"
        local grad="${gradient_green}\u@\h${gradient_light_green}\w${reset}"  # Green to light green gradient
        local sep="${bright_blue}${reset}"

        if shopt -q promptvars; then
            __powerline_git_info="$(__git_info)"
            local git="${cyan}\${__powerline_git_info}${reset}"
        else
            # promptvars is disabled. Avoid creating unnecessary env var.
            local git="${cyan}$(__git_info)$reset"
        fi

        PS1="${debian_chroot:+($debian_chroot)}$bright_blue$user_host$reset $cwd\n:$git $symbol"
    }

    PROMPT_COMMAND="ps1${PROMPT_COMMAND:+; $PROMPT_COMMAND}"
}

__powerline
unset __powerline
