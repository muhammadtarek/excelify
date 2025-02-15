const baseColors = {
  primary: '#0070E0',
  secondary: '#06BEE1',
  success: '#44AF69',
  warning: '#FCAB10',
  danger: '#F8333C',
  black: '#1b2733',
  grey: '#637282',
  light: '#f5f5f5',
  white: '#fff',
  transparent: 'transparent',
};

const COLORS = {
  BLUE: 'blue',
  SECONDARY: 'secondary',
  DANGER: 'danger',
  PAGE_BACKGROUND: 'pageBackground',
  SUCCESS: 'success',
  WARNING: 'warning',
  LINK: 'link',
  DISABLED: 'disabled',
  DISABLED_LIGHT: 'disabledLight',
  TEXT: 'text',
  HELP_TEXT: 'helpText',
  BORDER: 'border',
  HEADER: 'header',
  WHITE: 'white',
  SEPARATOR: 'separator',
  TRANSPARENT: 'transparent',
};

const COLORS_VALUES = {
  [COLORS.BLUE]: baseColors.primary,
  [COLORS.SECONDARY]: baseColors.secondary,
  [COLORS.DANGER]: baseColors.danger,
  [COLORS.PAGE_BACKGROUND]: baseColors.light,
  [COLORS.SUCCESS]: baseColors.success,
  [COLORS.WARNING]: baseColors.warning,
  [COLORS.LINK]: baseColors.primary,
  [COLORS.DISABLED]: baseColors.grey,
  [COLORS.DISABLED_LIGHT]: baseColors.light,
  [COLORS.TEXT]: baseColors.black,
  [COLORS.HELP_TEXT]: baseColors.grey,
  [COLORS.BORDER]: baseColors.light,
  [COLORS.HEADER]: baseColors.primary,
  [COLORS.WHITE]: baseColors.white,
  [COLORS.SEPARATOR]: baseColors.light,
};

export { COLORS, COLORS_VALUES };
export default COLORS;
