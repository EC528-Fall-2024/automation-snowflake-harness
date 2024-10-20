export type LanguageKeys = keyof typeof LANGUAGES

type LanguageObject<T> = {
  [Lang in LanguageKeys]: T
}

export const LANGUAGES = {
  en: 'English',
} as const

export type LandingPageObj = {
  description: string
  getStartedBtnText: string
  githubBtnText: string
}

export const LANDING_PAGE: LanguageObject<LandingPageObj> = {
  en: {
    description: 'Automate and streamline the management of Snowflake resources with CI/CD pipelines, leveraging Liquibase and Harness for secure and scalable deployments.',
    getStartedBtnText: 'Get started',
    githubBtnText: 'Source code',
  },
} as const

export const NAV: LanguageObject<{
  documentation: string
}> = {
  en: {
    documentation: 'Docs',
  },
} as const

export const ON_THIS_PAGE: LanguageObject<{
  onThisPage: string
  scrollToTop: string
}> = {
  en: {
    onThisPage: 'On this page',
    scrollToTop: 'Scroll to top',
  },
}

export const MISC: LanguageObject<{
  editThisPage: string
  previous: string
  next: string
}> = {
  en: {
    editThisPage: 'Edit this page',
    next: 'Next',
    previous: 'Previous',
  },
}

export const SEARCH: LanguageObject<{
  search: string
  keepTyping: string
  noResults: string
  results: string
}> = {
  en: {
    search: 'Search',
    keepTyping: 'Keep typing...',
    noResults: 'No results',
    results: 'Results',
  },
}
