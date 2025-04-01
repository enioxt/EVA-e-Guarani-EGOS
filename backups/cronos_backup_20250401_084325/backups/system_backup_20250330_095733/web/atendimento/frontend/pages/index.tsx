import Head from 'next/head'
import { useState } from 'react'

export default function Home() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implementar integração com backend
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-eva-background">
      <Head>
        <title>EVA Atendimento - Automatize seu WhatsApp com Amor e Ética</title>
        <meta name="description" content="EVA Atendimento - A solução inteligente e ética para automatizar seu atendimento no WhatsApp" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="max-w-7xl mx-auto">
            <div className="relative z-10 pb-8 bg-eva-background sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
              <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
                <div className="sm:text-center lg:text-left">
                  <h1 className="text-4xl tracking-tight font-extrabold text-eva-text sm:text-5xl md:text-6xl">
                    <span className="block">Automatize seu</span>
                    <span className="block text-eva-primary">WhatsApp com Amor</span>
                  </h1>
                  <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                    EVA Atendimento é a primeira solução de automação para WhatsApp que combina 
                    eficiência com ética e consciência. Mantenha seu atendimento humanizado mesmo quando automatizado.
                  </p>
                  <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                    {!submitted ? (
                      <form onSubmit={handleSubmit} className="sm:flex">
                        <input
                          type="email"
                          required
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="Seu melhor e-mail"
                          className="w-full px-5 py-3 border border-gray-300 shadow-sm placeholder-gray-400 focus:ring-1 focus:ring-eva-primary focus:border-eva-primary sm:max-w-xs rounded-md"
                        />
                        <div className="mt-3 sm:mt-0 sm:ml-3">
                          <button
                            type="submit"
                            className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-eva-primary hover:bg-eva-secondary md:py-4 md:text-lg md:px-10"
                          >
                            Entrar na lista de espera
                          </button>
                        </div>
                      </form>
                    ) : (
                      <div className="rounded-md bg-green-50 p-4">
                        <div className="flex">
                          <div className="ml-3">
                            <h3 className="text-sm font-medium text-green-800">
                              Obrigado pelo interesse!
                            </h3>
                            <div className="mt-2 text-sm text-green-700">
                              <p>
                                Em breve entraremos em contato com novidades.
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </main>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-12 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="lg:text-center">
              <h2 className="text-base text-eva-primary font-semibold tracking-wide uppercase">
                Benefícios
              </h2>
              <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-eva-text sm:text-4xl">
                Atendimento automatizado com consciência
              </p>
              <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
                Descubra como a EVA pode transformar seu atendimento mantendo a essência humana.
              </p>
            </div>

            <div className="mt-10">
              <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
                {features.map((feature) => (
                  <div key={feature.name} className="relative">
                    <dt>
                      <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-eva-primary text-white">
                        <feature.icon className="h-6 w-6" aria-hidden="true" />
                      </div>
                      <p className="ml-16 text-lg leading-6 font-medium text-eva-text">
                        {feature.name}
                      </p>
                    </dt>
                    <dd className="mt-2 ml-16 text-base text-gray-500">
                      {feature.description}
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 md:flex md:items-center md:justify-between lg:px-8">
          <div className="flex justify-center space-x-6 md:order-2">
            <p className="text-center text-base text-gray-400">
              &copy; 2024 EVA & GUARANI. Todos os direitos reservados.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

const features = [
  {
    name: 'Atendimento 24/7',
    description: 'Mantenha seu negócio funcionando mesmo quando você não está disponível.',
    icon: ClockIcon,
  },
  {
    name: 'Respostas Personalizadas',
    description: 'Cada cliente recebe um atendimento único, baseado em seu histórico e necessidades.',
    icon: UserIcon,
  },
  {
    name: 'Proteção de Dados',
    description: 'Seus dados e os de seus clientes são protegidos com os mais altos padrões éticos.',
    icon: ShieldCheckIcon,
  },
  {
    name: 'Integração Simples',
    description: 'Configure em minutos e comece a usar imediatamente.',
    icon: LightningBoltIcon,
  },
]

// Icons
function ClockIcon(props: any) {
  return (
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  )
}

function UserIcon(props: any) {
  return (
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  )
}

function ShieldCheckIcon(props: any) {
  return (
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
    </svg>
  )
}

function LightningBoltIcon(props: any) {
  return (
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
    </svg>
  )
} 