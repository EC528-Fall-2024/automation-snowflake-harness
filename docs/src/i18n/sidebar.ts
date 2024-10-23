import { type LanguageKeys } from '@/i18n/ui'

type SidebarSchema = {
  [Lang in LanguageKeys]: {
    introduction: string
    'getting-started': string
    'system-design-user': string
    'role-based-access-control': string
  }
}

export const SIDEBAR: SidebarSchema = {
  en: {
    introduction: 'Introduction',
    'getting-started': 'Getting started',
    'system-design-user': 'System Design and User Personas',
    'role-based-access-control': 'Role Based Access Control',
  },
}
