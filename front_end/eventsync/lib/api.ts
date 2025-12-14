// API configuration and helper functions for Django backend integration

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  senha: string
  cidade: string
  papel: "organizador" | "participante"
}

export interface Usuario {
  id: number
  username: string
  email: string
  papel: string
  cidade: string
  url_foto: string | null
}

export interface LoginResponse {
  refresh: string
  access: string
  usuario: Usuario
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
    this.name = "ApiError"
  }
}

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/autenticacao/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: "Erro ao fazer login" }))
      throw new ApiError(response.status, errorData.detail || errorData.message || "Credenciais inválidas")
    }

    const data: LoginResponse = await response.json()
    return data
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(0, "Erro de conexão com o servidor. Verifique sua conexão.")
  }
}

// Helper functions for token management
export function saveTokens(access: string, refresh: string) {
  localStorage.setItem("access_token", access)
  localStorage.setItem("refresh_token", refresh)
}

export function saveUser(usuario: Usuario) {
  localStorage.setItem("user", JSON.stringify(usuario))
}

export function clearAuth() {
  localStorage.removeItem("access_token")
  localStorage.removeItem("refresh_token")
  localStorage.removeItem("user")
}

export function getAccessToken(): string | null {
  return localStorage.getItem("access_token")
}

export function getUser(): Usuario | null {
  const userStr = localStorage.getItem("user")
  return userStr ? JSON.parse(userStr) : null
}

export async function register(data: RegisterData): Promise<Usuario> {
  try {
    const response = await fetch(`${API_BASE_URL}/autenticacao/registrar/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: "Erro ao criar conta" }))
      throw new ApiError(response.status, errorData.detail || errorData.message || "Erro ao criar conta")
    }

    const usuario: Usuario = await response.json()
    return usuario
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(0, "Erro de conexão com o servidor. Verifique sua conexão.")
  }
}
