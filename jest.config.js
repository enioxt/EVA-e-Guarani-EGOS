/** @type {import('jest').Config} */
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    rootDir: 'src',
    testMatch: ['**/*.test.ts'],
    transform: {
        '^.+\\.tsx?$': [
            'ts-jest',
            {
                isolatedModules: true,
                diagnostics: {
                    warnOnly: true
                }
            }
        ],
    },
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
    coverageDirectory: '../coverage',
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80,
        },
    },
    setupFilesAfterEnv: ['<rootDir>/core/mycelial/tests/setup.ts'],
    haste: {
        forceNodeFilesystemAPI: true,
        throwOnModuleCollision: false,
    },
    watchman: false,
}; 