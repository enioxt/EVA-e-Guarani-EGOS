import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        tsconfigPaths()
    ],
    resolve: {
        alias: {
            '@': resolve(__dirname, './src'),
            '@components': resolve(__dirname, './src/components'),
            '@hooks': resolve(__dirname, './src/hooks'),
            '@utils': resolve(__dirname, './src/utils'),
            '@services': resolve(__dirname, './src/services'),
            '@styles': resolve(__dirname, './src/styles'),
            '@assets': resolve(__dirname, './src/assets'),
            '@types': resolve(__dirname, './src/types'),
            '@config': resolve(__dirname, './src/config'),
            '@constants': resolve(__dirname, './src/constants'),
            '@contexts': resolve(__dirname, './src/contexts'),
            '@layouts': resolve(__dirname, './src/layouts'),
            '@pages': resolve(__dirname, './src/pages'),
            '@store': resolve(__dirname, './src/store'),
            '@api': resolve(__dirname, './src/api'),
            '@tests': resolve(__dirname, './src/tests')
        }
    },
    server: {
        port: 3000,
        host: true,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                secure: false,
                ws: true
            }
        }
    },
    preview: {
        port: 3000,
        host: true
    },
    build: {
        outDir: 'dist',
        sourcemap: true,
        manifest: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html')
            },
            output: {
                manualChunks: {
                    'react-vendor': ['react', 'react-dom'],
                    'd3-vendor': ['d3'],
                    'lodash-vendor': ['lodash']
                }
            }
        }
    },
    optimizeDeps: {
        include: ['react', 'react-dom', 'd3', 'lodash'],
        exclude: ['@testing-library/react']
    },
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: ['./src/tests/setup.ts'],
        coverage: {
            reporter: ['text', 'json', 'html'],
            exclude: [
                'node_modules/',
                'src/tests/',
                '**/*.d.ts',
                '**/*.test.{ts,tsx}',
                '**/*.spec.{ts,tsx}'
            ]
        }
    },
    css: {
        modules: {
            localsConvention: 'camelCase'
        },
        preprocessorOptions: {
            scss: {
                additionalData: `@import "@styles/variables.scss";`
            }
        }
    }
})
