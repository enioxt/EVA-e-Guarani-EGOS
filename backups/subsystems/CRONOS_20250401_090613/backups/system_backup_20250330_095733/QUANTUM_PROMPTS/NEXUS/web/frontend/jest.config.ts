import type { Config } from '@jest/types'
import { pathsToModuleNameMapper } from 'ts-jest'
import { compilerOptions } from './tsconfig.json'

const config: Config.InitialOptions = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    roots: ['<rootDir>/src'],
    transform: {
        '^.+\\.tsx?$': 'ts-jest',
        '^.+\\.jsx?$': 'babel-jest',
        '.+\\.(css|styl|less|sass|scss)$': 'jest-transform-css',
        '.+\\.(jpg|jpeg|png|gif|webp|svg)$': 'jest-transform-file'
    },
    setupFilesAfterEnv: ['<rootDir>/src/tests/setup.ts'],
    testRegex: '(/__tests__/.*|(\\.|/)(test|spec))\\.tsx?$',
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
    moduleNameMapper: {
        ...pathsToModuleNameMapper(compilerOptions.paths, { prefix: '<rootDir>/src' }),
        '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
        '\\.(gif|ttf|eot|svg|png)$': '<rootDir>/src/tests/__mocks__/fileMock.ts'
    },
    collectCoverage: true,
    collectCoverageFrom: [
        'src/**/*.{ts,tsx}',
        '!src/**/*.d.ts',
        '!src/**/*.stories.{ts,tsx}',
        '!src/**/*.test.{ts,tsx}',
        '!src/**/*.spec.{ts,tsx}',
        '!src/tests/**/*',
        '!src/types/**/*'
    ],
    coverageDirectory: 'coverage',
    coverageReporters: ['json', 'lcov', 'text', 'clover'],
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80
        }
    },
    globals: {
        'ts-jest': {
            tsconfig: 'tsconfig.json',
            diagnostics: true,
            isolatedModules: true
        }
    },
    verbose: true,
    testTimeout: 10000,
    maxWorkers: '50%',
    watchPlugins: [
        'jest-watch-typeahead/filename',
        'jest-watch-typeahead/testname'
    ],
    clearMocks: true,
    resetMocks: false,
    restoreMocks: true,
    errorOnDeprecated: true,
    notify: true,
    notifyMode: 'failure-change',
    bail: 1,
    cache: true,
    cacheDirectory: '.jest-cache',
    detectLeaks: true,
    detectOpenHandles: true,
    passWithNoTests: false,
    randomize: true,
    runInBand: false,
    testLocationInResults: true,
    timers: 'modern'
}
