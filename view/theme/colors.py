"""
Sistema de cores moderno para a Agenda Virtual
Paleta inspirada em design systems modernos com foco em acessibilidade
"""

class ColorPalette:
    """Paleta de cores moderna e acessível"""
    
    # Cores primárias
    PRIMARY = {
        'main': '#2563eb',      # Azul principal
        'light': '#3b82f6',     # Azul claro
        'dark': '#1d4ed8',      # Azul escuro
        'contrast': '#ffffff'   # Texto sobre azul
    }
    
    # Cores secundárias
    SECONDARY = {
        'main': '#7c3aed',      # Roxo principal
        'light': '#8b5cf6',     # Roxo claro
        'dark': '#6d28d9',      # Roxo escuro
        'contrast': '#ffffff'   # Texto sobre roxo
    }
    
    # Cores de sucesso
    SUCCESS = {
        'main': '#059669',      # Verde principal
        'light': '#10b981',     # Verde claro
        'dark': '#047857',      # Verde escuro
        'contrast': '#ffffff'   # Texto sobre verde
    }
    
    # Cores de aviso
    WARNING = {
        'main': '#d97706',      # Laranja principal
        'light': '#f59e0b',     # Laranja claro
        'dark': '#b45309',      # Laranja escuro
        'contrast': '#ffffff'   # Texto sobre laranja
    }
    
    # Cores de erro
    ERROR = {
        'main': '#dc2626',      # Vermelho principal
        'light': '#ef4444',     # Vermelho claro
        'dark': '#b91c1c',      # Vermelho escuro
        'contrast': '#ffffff'   # Texto sobre vermelho
    }
    
    # Cores neutras
    NEUTRAL = {
        'white': '#ffffff',
        'gray_50': '#f9fafb',
        'gray_100': '#f3f4f6',
        'gray_200': '#e5e7eb',
        'gray_300': '#d1d5db',
        'gray_400': '#9ca3af',
        'gray_500': '#6b7280',
        'gray_600': '#4b5563',
        'gray_700': '#374151',
        'gray_800': '#1f2937',
        'gray_900': '#111827',
        'black': '#000000'
    }
    
    # Cores de fundo
    BACKGROUND = {
        'primary': NEUTRAL['white'],
        'secondary': NEUTRAL['gray_50'],
        'tertiary': NEUTRAL['gray_100'],
        'card': NEUTRAL['white'],
        'overlay': 'rgba(0, 0, 0, 0.5)'
    }
    
    # Cores de texto
    TEXT = {
        'primary': NEUTRAL['gray_900'],
        'secondary': NEUTRAL['gray_600'],
        'tertiary': NEUTRAL['gray_500'],
        'disabled': NEUTRAL['gray_400'],
        'inverse': NEUTRAL['white']
    }
    
    # Cores de borda
    BORDER = {
        'light': NEUTRAL['gray_200'],
        'medium': NEUTRAL['gray_300'],
        'dark': NEUTRAL['gray_400'],
        'focus': PRIMARY['main']
    }
    
    # Cores de sombra
    SHADOW = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
    }

class PriorityColors:
    """Cores específicas para prioridades de tarefas"""
    
    COLORS = {
        'MUITO_IMPORTANTE': {
            'main': ColorPalette.ERROR['main'],
            'light': ColorPalette.ERROR['light'],
            'background': '#fef2f2',
            'border': '#fecaca'
        },
        'IMPORTANTE': {
            'main': ColorPalette.WARNING['main'],
            'light': ColorPalette.WARNING['light'],
            'background': '#fffbeb',
            'border': '#fed7aa'
        },
        'MEDIA': {
            'main': ColorPalette.SECONDARY['main'],
            'light': ColorPalette.SECONDARY['light'],
            'background': '#faf5ff',
            'border': '#e9d5ff'
        },
        'SIMPLES': {
            'main': ColorPalette.SUCCESS['main'],
            'light': ColorPalette.SUCCESS['light'],
            'background': '#f0fdf4',
            'border': '#bbf7d0'
        },
        'EVENTO': {
            'main': ColorPalette.PRIMARY['main'],
            'light': ColorPalette.PRIMARY['light'],
            'background': '#eff6ff',
            'border': '#bfdbfe'
        },
        'GERAL': {
            'main': ColorPalette.NEUTRAL['gray_600'],
            'light': ColorPalette.NEUTRAL['gray_500'],
            'background': ColorPalette.NEUTRAL['gray_50'],
            'border': ColorPalette.NEUTRAL['gray_200']
        }
    }
    
    @classmethod
    def get_color(cls, priority, variant='main'):
        """Obter cor para uma prioridade específica"""
        priority_colors = cls.COLORS.get(priority, cls.COLORS['GERAL'])
        return priority_colors.get(variant, priority_colors['main'])

class StatusColors:
    """Cores para status de tarefas"""
    
    COLORS = {
        'completed': {
            'main': ColorPalette.SUCCESS['main'],
            'background': ColorPalette.SUCCESS['light'],
            'text': ColorPalette.SUCCESS['contrast']
        },
        'pending': {
            'main': ColorPalette.WARNING['main'],
            'background': ColorPalette.WARNING['light'],
            'text': ColorPalette.WARNING['contrast']
        },
        'in_progress': {
            'main': ColorPalette.PRIMARY['main'],
            'background': ColorPalette.PRIMARY['light'],
            'text': ColorPalette.PRIMARY['contrast']
        },
        'overdue': {
            'main': ColorPalette.ERROR['main'],
            'background': ColorPalette.ERROR['light'],
            'text': ColorPalette.ERROR['contrast']
        }
    }
    
    @classmethod
    def get_color(cls, status, variant='main'):
        """Obter cor para um status específico"""
        status_colors = cls.COLORS.get(status, cls.COLORS['pending'])
        return status_colors.get(variant, status_colors['main'])

class TypeColors:
    """Cores para tipos de itens"""
    
    COLORS = {
        'task': {
            'main': ColorPalette.PRIMARY['main'],
            'background': ColorPalette.PRIMARY['light'],
            'text': ColorPalette.PRIMARY['contrast']
        },
        'event': {
            'main': ColorPalette.SECONDARY['main'],
            'background': ColorPalette.SECONDARY['light'],
            'text': ColorPalette.SECONDARY['contrast']
        },
        'appointment': {
            'main': ColorPalette.SUCCESS['main'],
            'background': ColorPalette.SUCCESS['light'],
            'text': ColorPalette.SUCCESS['contrast']
        },
        'reminder': {
            'main': ColorPalette.WARNING['main'],
            'background': ColorPalette.WARNING['light'],
            'text': ColorPalette.WARNING['contrast']
        }
    }
    
    @classmethod
    def get_color(cls, item_type, variant='main'):
        """Obter cor para um tipo específico"""
        type_colors = cls.COLORS.get(item_type, cls.COLORS['task'])
        return type_colors.get(variant, type_colors['main']) 