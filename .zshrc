if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="$HOME/.oh-my-zsh"
export ZSH_THEME="powerlevel10k/powerlevel10k"
export HISTSIZE=100000
export SAVEHIST=100000

export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

plugins=(
  git
  zsh-syntax-highlighting
  zsh-autosuggestions
  docker
)

source $ZSH/oh-my-zsh.sh

if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'
else
  export EDITOR='nvim'
fi

if [[ $- == *i* ]]; then
  git-currentbranch-paste() {
    LBUFFER="$LBUFFER$(git rev-parse --abbrev-ref HEAD)"
    local ret=$?
    zle redisplay
    typeset -f zle-line-init >/dev/null && zle zle-line-init
    return $ret
  }
  zle     -N   git-currentbranch-paste
  bindkey '^B' git-currentbranch-paste

  goto-workplace() {
    directories=(
      ~/Work 
      ~/Work/zewotherm 
      ~/Work/projects 
      ~/Work/mc 
      ~/Work/etc 
      ~/.config 
      ~/ 
      ~/Uni
    )

    selected_dirs=$(find "$directories[@]" -mindepth 1 -maxdepth 1 -type d | fzf)
    if [ -n "$selected_dirs" ]; then
      cd "$selected_dirs"
      zle accept-line
      zle reset-prompt
    fi
  }

  zle     -N   goto-workplace
  bindkey '^F' goto-workplace
fi

export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

alias ls='EXA_ICON_SPACING=2 exa --icons --group-directories-first'
alias ll='ls -l'
alias la='ll -a'
alias llm='ll --sort modified'
alias lm='l --sort modified'
alias lam='la --sort modified'
alias vim=nvim
alias sail='[ -f sail ] && sh sail || sh vendor/bin/sail'
alias gs='git status'
alias gla='git log --oneline --graph --decorate --all --color'
alias gpo='git push origin'
alias dotfiles="/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME"

ssh-add --apple-use-keychain ~/.ssh/id_rsa 2>/dev/null

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

[ -f "/Users/florian/.ghcup/env" ] && source "/Users/florian/.ghcup/env" # ghcup-env

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/private/etc/google-cloud-sdk/path.zsh.inc' ]; then . '/private/etc/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/private/etc/google-cloud-sdk/completion.zsh.inc' ]; then . '/private/etc/google-cloud-sdk/completion.zsh.inc'; fi

export GOOGLE_APPLICATION_CREDENTIALS='/Users/florian/.config/gcloud/application_default_credentials.json'

# Set up fzf key bindings and fuzzy completion
eval "$(fzf --zsh)"

if [ -f "$HOME/.secrets.zsh" ]; then source "$HOME/.secrets.zsh"; fi
