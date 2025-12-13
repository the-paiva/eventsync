import Link from "next/link"
import { Calendar, Users, MapPin, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calendar className="w-6 h-6 text-primary" />
            <span className="font-bold text-xl">EventSync</span>
          </div>
          <nav className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/registro">
              <Button>Cadastrar</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium mb-6">
              <Sparkles className="w-4 h-4" />
              <span>Gerencie eventos com inteligência artificial</span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6 text-balance">
              Organize eventos incríveis com <span className="text-primary">EventSync</span>
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground mb-8 text-balance">
              A plataforma completa para criar, gerenciar e promover seus eventos. Conecte pessoas, simplifique
              processos e garanta o sucesso dos seus eventos.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/registro">
                <Button size="lg" className="w-full sm:w-auto">
                  Começar agora
                </Button>
              </Link>
              <Link href="/login">
                <Button size="lg" variant="outline" className="w-full sm:w-auto bg-transparent">
                  Fazer login
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-4 py-16 border-t border-border">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mb-4">
                <Calendar className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Gestão Completa</h3>
              <p className="text-muted-foreground text-sm">
                Gerencie todos os aspectos dos seus eventos em um único lugar
              </p>
            </div>

            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mb-4">
                <Users className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Controle de Participantes</h3>
              <p className="text-muted-foreground text-sm">
                Gerencie inscrições e acompanhe participantes em tempo real
              </p>
            </div>

            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 rounded-lg mb-4">
                <MapPin className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Eventos Locais</h3>
              <p className="text-muted-foreground text-sm">Descubra e participe de eventos na sua cidade</p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>© 2025 EventSync. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  )
}
