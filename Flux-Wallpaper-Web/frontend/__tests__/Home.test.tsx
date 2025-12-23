
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Home from '../app/page'

// Mock components that might cause issues in simple unit tests (like Three.js or complex animations)
jest.mock('@/components/sections/hero', () => ({
  HeroSection: () => <div data-testid="hero-section">Hero Section</div>
}))
jest.mock('@/components/sections/stats', () => ({
  StatsSection: () => <div data-testid="stats-section">Stats Section</div>
}))
jest.mock('@/components/ui/navbar', () => ({
  Navbar: () => <div data-testid="navbar">Navbar</div>
}))
jest.mock('@/components/ui/footer', () => ({
  Footer: () => <div data-testid="footer">Footer</div>
}))

describe('Home Page', () => {
  it('renders correctly', () => {
    render(<Home />)
 
    expect(screen.getByTestId('navbar')).toBeInTheDocument()
    expect(screen.getByTestId('hero-section')).toBeInTheDocument()
    expect(screen.getByText('How It Works')).toBeInTheDocument()
    expect(screen.getByText('Ready to create in 3D?')).toBeInTheDocument()
  })
})
