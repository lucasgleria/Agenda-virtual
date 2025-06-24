"""
Configuração de estilos para a Agenda Virtual
Aplica a nova paleta de cores de forma consistente
"""

import tkinter as tk
from tkinter import ttk
from .colors import ColorPalette

class StyleManager:
    """Gerenciador de estilos para a aplicação"""
    
    @staticmethod
    def setup_styles():
        """Configurar estilos personalizados"""
        style = ttk.Style()
        
        # Configurar tema base
        try:
            style.theme_use('clam')  # Tema mais moderno
        except:
            try:
                style.theme_use('vista')
            except:
                style.theme_use('default')
        
        # Configurar cores base
        style.configure('.',
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       fieldbackground=ColorPalette.BACKGROUND['secondary'],
                       troughcolor=ColorPalette.BACKGROUND['tertiary'],
                       selectbackground=ColorPalette.PRIMARY['main'],
                       selectforeground=ColorPalette.TEXT['inverse'])
        
        # Estilo para botões primários
        style.configure('Primary.TButton',
                       background=ColorPalette.PRIMARY['main'],
                       foreground=ColorPalette.TEXT['inverse'],
                       bordercolor=ColorPalette.PRIMARY['main'],
                       focuscolor=ColorPalette.PRIMARY['light'])
        
        # Estilo para botões de sucesso
        style.configure('Success.TButton',
                       background=ColorPalette.SUCCESS['main'],
                       foreground=ColorPalette.TEXT['inverse'],
                       bordercolor=ColorPalette.SUCCESS['main'],
                       focuscolor=ColorPalette.SUCCESS['light'])
        
        # Estilo para botões de aviso
        style.configure('Warning.TButton',
                       background=ColorPalette.WARNING['main'],
                       foreground=ColorPalette.TEXT['inverse'],
                       bordercolor=ColorPalette.WARNING['main'],
                       focuscolor=ColorPalette.WARNING['light'])
        
        # Estilo para botões de erro
        style.configure('Error.TButton',
                       background=ColorPalette.ERROR['main'],
                       foreground=ColorPalette.TEXT['inverse'],
                       bordercolor=ColorPalette.ERROR['main'],
                       focuscolor=ColorPalette.ERROR['light'])
        
        # Estilo para botões secundários
        style.configure('Secondary.TButton',
                       background=ColorPalette.SECONDARY['main'],
                       foreground=ColorPalette.TEXT['inverse'],
                       bordercolor=ColorPalette.SECONDARY['main'],
                       focuscolor=ColorPalette.SECONDARY['light'])
        
        # Estilo para botões de destaque
        style.configure('Accent.TButton',
                       background=ColorPalette.PRIMARY['main'],
                       foreground=ColorPalette.TEXT['inverse'],
                       bordercolor=ColorPalette.PRIMARY['main'],
                       focuscolor=ColorPalette.PRIMARY['light'],
                       font=('Segoe UI', 9, 'bold'))
        
        # Estilo para labels de título
        style.configure('Title.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=ColorPalette.TEXT['primary'])
        
        # Estilo para labels de subtítulo
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=ColorPalette.TEXT['secondary'])
        
        # Estilo para labels de texto
        style.configure('Text.TLabel',
                       font=('Segoe UI', 10),
                       foreground=ColorPalette.TEXT['primary'])
        
        # Estilo para labels de texto secundário
        style.configure('TextSecondary.TLabel',
                       font=('Segoe UI', 9),
                       foreground=ColorPalette.TEXT['secondary'])
        
        # Estilo para frames de card
        style.configure('Card.TFrame',
                       background=ColorPalette.BACKGROUND['card'],
                       relief='solid',
                       borderwidth=1)
        
        # Estilo para frames de painel
        style.configure('Panel.TFrame',
                       background=ColorPalette.BACKGROUND['secondary'],
                       relief='solid',
                       borderwidth=1)
        
        # Estilo para comboboxes
        style.configure('TCombobox',
                       fieldbackground=ColorPalette.BACKGROUND['secondary'],
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       arrowcolor=ColorPalette.TEXT['secondary'],
                       bordercolor=ColorPalette.BORDER['medium'],
                       focuscolor=ColorPalette.PRIMARY['main'])
        
        # Estilo para entries
        style.configure('TEntry',
                       fieldbackground=ColorPalette.BACKGROUND['secondary'],
                       foreground=ColorPalette.TEXT['primary'],
                       bordercolor=ColorPalette.BORDER['medium'],
                       focuscolor=ColorPalette.PRIMARY['main'])
        
        # Estilo para treeview
        style.configure('Treeview',
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       fieldbackground=ColorPalette.BACKGROUND['primary'],
                       bordercolor=ColorPalette.BORDER['light'],
                       focuscolor=ColorPalette.PRIMARY['main'])
        
        style.configure('Treeview.Heading',
                       background=ColorPalette.BACKGROUND['secondary'],
                       foreground=ColorPalette.TEXT['primary'],
                       bordercolor=ColorPalette.BORDER['medium'],
                       font=('Segoe UI', 9, 'bold'))
        
        # Estilo para scrollbars
        style.configure('TScrollbar',
                       background=ColorPalette.BACKGROUND['tertiary'],
                       bordercolor=ColorPalette.BORDER['light'],
                       arrowcolor=ColorPalette.TEXT['secondary'],
                       troughcolor=ColorPalette.BACKGROUND['secondary'])
        
        # Estilo para notebooks (abas)
        style.configure('TNotebook',
                       background=ColorPalette.BACKGROUND['primary'],
                       bordercolor=ColorPalette.BORDER['light'])
        
        style.configure('TNotebook.Tab',
                       background=ColorPalette.BACKGROUND['secondary'],
                       foreground=ColorPalette.TEXT['primary'],
                       bordercolor=ColorPalette.BORDER['light'],
                       focuscolor=ColorPalette.PRIMARY['main'],
                       padding=[10, 5])
        
        # Estilo para labelframes
        style.configure('TLabelframe',
                       background=ColorPalette.BACKGROUND['primary'],
                       bordercolor=ColorPalette.BORDER['medium'])
        
        style.configure('TLabelframe.Label',
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Estilo para checkbuttons
        style.configure('TCheckbutton',
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       focuscolor=ColorPalette.PRIMARY['main'])
        
        # Estilo para radiobuttons
        style.configure('TRadiobutton',
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       focuscolor=ColorPalette.PRIMARY['main'])
        
        # Estilo para separators
        style.configure('TSeparator',
                       background=ColorPalette.BORDER['light'])
        
        # Estilo para progressbars
        style.configure('TProgressbar',
                       background=ColorPalette.PRIMARY['main'],
                       bordercolor=ColorPalette.PRIMARY['main'],
                       lightcolor=ColorPalette.PRIMARY['light'],
                       darkcolor=ColorPalette.PRIMARY['dark'],
                       troughcolor=ColorPalette.BACKGROUND['secondary'])
        
        # Estilo para spinboxes
        style.configure('TSpinbox',
                       fieldbackground=ColorPalette.BACKGROUND['secondary'],
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       bordercolor=ColorPalette.BORDER['medium'],
                       focuscolor=ColorPalette.PRIMARY['main'],
                       arrowcolor=ColorPalette.TEXT['secondary'])
        
        # Estilo para scales
        style.configure('TScale',
                       background=ColorPalette.BACKGROUND['primary'],
                       foreground=ColorPalette.TEXT['primary'],
                       bordercolor=ColorPalette.BORDER['light'],
                       troughcolor=ColorPalette.BACKGROUND['secondary'],
                       slidercolor=ColorPalette.PRIMARY['main'])
        
        # Estilo para paned windows
        style.configure('TPanedwindow',
                       background=ColorPalette.BACKGROUND['primary'],
                       bordercolor=ColorPalette.BORDER['light'])
        
        # Estilo para sizegrip
        style.configure('TSizegrip',
                       background=ColorPalette.BACKGROUND['tertiary'],
                       bordercolor=ColorPalette.BORDER['light'])
        
        # Estilo para tooltips (se disponível)
        try:
            style.configure('Tooltip.TLabel',
                           background=ColorPalette.NEUTRAL['gray_800'],
                           foreground=ColorPalette.TEXT['inverse'],
                           bordercolor=ColorPalette.BORDER['dark'],
                           font=('Segoe UI', 8))
        except:
            pass
    
    @staticmethod
    def apply_priority_colors(tree, priority_colors):
        """Aplicar cores de prioridade ao treeview"""
        for priority, color in priority_colors.items():
            tree.tag_configure(priority, foreground=color)
    
    @staticmethod
    def apply_status_colors(tree, status_colors):
        """Aplicar cores de status ao treeview"""
        for status, color in status_colors.items():
            tree.tag_configure(status, foreground=color)
    
    @staticmethod
    def get_button_style(priority='primary'):
        """Obter estilo de botão baseado na prioridade"""
        styles = {
            'primary': 'Primary.TButton',
            'success': 'Success.TButton',
            'warning': 'Warning.TButton',
            'error': 'Error.TButton',
            'secondary': 'Secondary.TButton',
            'accent': 'Accent.TButton'
        }
        return styles.get(priority, 'TButton')
    
    @staticmethod
    def get_label_style(style_type='text'):
        """Obter estilo de label baseado no tipo"""
        styles = {
            'title': 'Title.TLabel',
            'subtitle': 'Subtitle.TLabel',
            'text': 'Text.TLabel',
            'text_secondary': 'TextSecondary.TLabel'
        }
        return styles.get(style_type, 'TLabel') 