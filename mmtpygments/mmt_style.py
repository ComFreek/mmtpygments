from pygments.token import Token
from pygments.styles.default import DefaultStyle

__all__ = ['MMTDefaultStyle']

class MMTDefaultStyle(DefaultStyle):
	background_color = DefaultStyle.background_color
	default_style = DefaultStyle.default_style

	_default_styles = DefaultStyle.styles.copy()
	_default_styles[Token.MMT_MD] = '#D3D3D3'
	_default_styles[Token.MMT_DD] = '#D3D3D3'
	_default_styles[Token.MMT_OD] = '#D3D3D3'

	styles = _default_styles
