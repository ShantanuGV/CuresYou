import React, { useState, useEffect, useRef } from 'react';
import './index.css';
import logo from "./assets/curseyou_logo.png";
import header from "./assets/curseyou_header.png";
import hero from "./assets/curseyou_hero.png";
import footer from "./assets/thankyou_footer.png";
// Wiggly, organic-styled vector paths for the letters A-Z (viewBox="0 0 400 500")
const GLYPH_PATHS = {
  A: "M 200 60 L 90 400 M 200 60 L 310 400 M 130 290 L 270 290",
  B: "M 120 80 L 120 420 M 120 80 C 280 80 280 230 120 230 C 290 230 290 420 120 420",
  C: "M 320 140 C 200 90 90 170 90 250 C 90 330 200 410 320 360",
  D: "M 120 80 L 120 420 C 310 420 310 80 120 80",
  E: "M 300 80 L 120 80 L 120 420 L 320 420 M 120 250 L 270 250",
  F: "M 300 80 L 120 80 L 120 420 M 120 250 L 260 250",
  G: "M 320 150 C 210 90 100 170 100 250 C 100 330 200 410 310 360 L 310 260 L 220 260",
  H: "M 100 80 L 100 420 M 300 80 L 300 420 M 100 250 L 300 250",
  I: "M 150 80 L 250 80 M 200 80 L 200 420 M 150 420 L 250 420",
  J: "M 250 80 L 250 330 C 250 400 140 430 100 360",
  K: "M 120 80 L 120 420 M 300 80 L 120 250 L 300 420",
  L: "M 120 80 L 120 420 L 300 420",
  M: "M 80 420 L 80 80 L 200 260 L 320 80 L 320 420",
  N: "M 90 420 L 90 80 L 310 420 L 310 80",
  O: "M 200 80 C 310 80 310 420 200 420 C 90 420 90 80 200 80 Z",
  P: "M 120 80 L 120 420 M 120 80 C 280 80 280 250 120 250",
  Q: "M 200 80 C 310 80 310 380 200 380 C 90 380 90 80 200 80 Z M 250 330 L 320 420",
  R: "M 120 80 L 120 420 M 120 80 C 280 80 280 230 120 230 L 300 420",
  S: "M 290 120 C 230 70 110 120 170 200 C 250 280 280 330 220 380 C 140 430 90 350 90 350",
  T: "M 90 80 L 310 80 M 200 80 L 200 420",
  U: "M 100 80 L 100 340 C 100 420 300 420 300 340 L 300 80",
  V: "M 90 80 L 200 420 L 310 80",
  W: "M 80 80 L 130 420 L 200 220 L 270 420 L 320 80",
  X: "M 90 80 L 310 420 M 310 80 L 90 420",
  Y: "M 90 80 L 200 240 L 310 80 M 200 240 L 200 420",
  Z: "M 90 80 L 310 80 L 90 420 L 310 420"
};

const KEYBOARD_ROWS = [
  { keys: ["A", "B", "C", "D", "E", "F", "G", "H"], staggered: false },
  { keys: ["I", "J", "K", "L", "M", "N", "O", "P"], staggered: true },
  { keys: ["Q", "R", "S", "T", "U", "V", "W", "X"], staggered: false },
  { keys: ["Y", "Z"], staggered: true }
];

const RANDOM_NAMES = ['Rakesh', 'Shantanu', 'Gaurav', 'Aditay', 'Shivam', 'Bhavik', 'Aayush', 'Sachit'];

function App() {
  const [activeSection, setActiveSection] = useState('');
  
  // Choose initial random name
  const [tryText, setTryText] = useState(() => {
    return RANDOM_NAMES[Math.floor(Math.random() * RANDOM_NAMES.length)].toUpperCase();
  });
  
  // Typewriter effect state for placeholder
  const [placeholderText, setPlaceholderText] = useState('');
  
  // States for backend generated image
  const [generatedImage, setGeneratedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);

  // States for GLYPH text
  const [glyphText, setGlyphText] = useState('C');
  const [activeKey, setActiveKey] = useState('C');
  const [isScrolled, setIsScrolled] = useState(false);

  const navRef = useRef(null);
  const parallaxBgRef = useRef(null);

  // Typewriter placeholder animation loop
  useEffect(() => {
    let currentWordIndex = 0;
    let currentCharIndex = 0;
    let isDeleting = false;
    let timerId = null;

    const typeEffect = () => {
      const currentWord = RANDOM_NAMES[currentWordIndex];

      if (isDeleting) {
        setPlaceholderText(currentWord.substring(0, currentCharIndex - 1));
        currentCharIndex--;
      } else {
        setPlaceholderText(currentWord.substring(0, currentCharIndex + 1));
        currentCharIndex++;
      }

      let speed = isDeleting ? 80 : 150;

      if (!isDeleting && currentCharIndex === currentWord.length) {
        isDeleting = true;
        speed = 2200; // Pause at the fully typed name
      } else if (isDeleting && currentCharIndex === 0) {
        isDeleting = false;
        currentWordIndex = (currentWordIndex + 1) % RANDOM_NAMES.length;
        speed = 500; // Pause before typing the next name
      }

      timerId = setTimeout(typeEffect, speed);
    };

    timerId = setTimeout(typeEffect, 400);

    return () => clearTimeout(timerId);
  }, []);

  // Scroll event listeners for Parallax and Header transition
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;

      // 1. Smooth Parallax background translation (scrolling UP)
      if (parallaxBgRef.current) {
        parallaxBgRef.current.style.transform = `translate3d(0, ${-scrollY * 0.15}px, 0)`;
      }

      // 2. Dynamic state for sticky navbar and logo transition
      if (scrollY > 120) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }

      // 3. Active section link highlighting
      const sections = ['about', 'try', 'glyph', 'architecture'];
      let currentSection = '';
      
      for (const sectionId of sections) {
        const element = document.getElementById(sectionId);
        if (element) {
          const rect = element.getBoundingClientRect();
          // If the top of the section is near the center/top of viewport
          if (rect.top <= 200 && rect.bottom >= 200) {
            currentSection = sectionId;
            break;
          }
        }
      }

      // If scrolling at the very top, clear active selection (Hero is visible)
      if (scrollY < 150) {
        currentSection = '';
      }

      setActiveSection(currentSection);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    // Trigger once to initialize
    handleScroll();

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Debounced API call to backend when name is entered in TRY section
  useEffect(() => {
    let active = true;

    if (!tryText || tryText.trim() === '') {
      setGeneratedImage(null);
      setApiError(null);
      return;
    }

    const delayDebounceFn = setTimeout(() => {
      setIsLoading(true);
      setApiError(null);

    const API_URL = "https://curesyou.onrender.com";

    fetch(`${API_URL}/api/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ word: tryText }),
      })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((data) => {
            throw new Error(data.error || 'Failed to generate image');
          });
        }
        return res.blob();
      })
      .then((blob) => {
        if (active) {
          // Revoke old URL if present to prevent memory leaks
          if (generatedImage) {
            URL.revokeObjectURL(generatedImage);
          }
          const url = URL.createObjectURL(blob);
          setGeneratedImage(url);
        }
      })
      .catch((err) => {
        if (active) {
          console.error('API Error:', err);
          setApiError(err.message);
        }
      })
      .finally(() => {
        if (active) {
          setIsLoading(false);
        }
      });
    }, 850); // 850ms debounce delay

    return () => {
      active = false;
      clearTimeout(delayDebounceFn);
    };
  }, [tryText]);

  // Download generated image from blob URL
  const handleDownloadImage = () => {
    if (generatedImage) {
      const link = document.createElement('a');
      link.href = generatedImage;
      link.download = `${tryText.toLowerCase()}_river.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  // Reset name selection to a new random name
  const handleResetName = () => {
    let currentName = tryText;
    let newName = currentName;
    // Make sure we select a different name than current
    while (newName === currentName) {
      newName = RANDOM_NAMES[Math.floor(Math.random() * RANDOM_NAMES.length)].toUpperCase();
    }
    setTryText(newName);
  };

  // Handle keys clicked on custom keyboard
  const handleHexKeyClick = (key) => {
    setActiveKey(key);
    setGlyphText((prev) => prev + key);
  };

  // Download GLYPH text string
  const handleDownloadTxt = () => {
    const element = document.createElement("a");
    const file = new Blob([glyphText], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "glyph_sequence.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Download active letter SVG
  const handleDownloadLetterImage = () => {
    if (!activeKey || !GLYPH_PATHS[activeKey]) return;
    const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
      <rect width="100%" height="100%" fill="#122117"/>
      <!-- Guides -->
      <line x1="0" y1="125" x2="400" y2="125" stroke="#ffffff" stroke-width="2" stroke-dasharray="5,5" opacity="0.15"/>
      <line x1="0" y1="250" x2="400" y2="250" stroke="#ffffff" stroke-width="2" stroke-dasharray="5,5" opacity="0.15"/>
      <line x1="0" y1="375" x2="400" y2="375" stroke="#ffffff" stroke-width="2" stroke-dasharray="5,5" opacity="0.15"/>
      <!-- Glyph -->
      <path d="${GLYPH_PATHS[activeKey]}" fill="none" stroke="#a3d900" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
    const element = document.createElement("a");
    const file = new Blob([svgContent], {type: 'image/svg+xml'});
    element.href = URL.createObjectURL(file);
    element.download = `glyph_letter_${activeKey}.svg`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Scroll to section manually
  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <>
      {/* 
        INJECTING CUSTOM STYLES
        We inject styles here to maintain the locked src/index.css unchanged,
        while updating background scaling, the about layout, and the step-by-step timeline.
      */}
      

      {/* SVG filter definitions for organic wiggle effect */}
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <defs>
          <filter id="organic-wobble">
            <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" result="noise" />
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="14" xChannelSelector="R" yChannelSelector="G" />
          </filter>
        </defs>
      </svg>

      {/* Parallax Background */}
      <div ref={parallaxBgRef} className="parallax-bg" />

      {/* Header / Sticky Navigation */}
      <nav ref={navRef} className={`header-nav ${isScrolled ? 'scrolled' : ''} ${isMobileMenuOpen ? 'mobile-nav-open' : ''}`} id="main-nav">
        <div className="logo-container" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <img src={logo} alt="C" className="logo-symbol-img" />
          <span className="mobile-nav-title">CURSEYOU - CURVY GEO-SCRIPT</span>
        </div>

        <button 
          className="menu-toggle" 
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="Toggle Menu"
        >
          ☰
        </button>

        <ul className={`nav-links ${isMobileMenuOpen ? 'mobile-open' : ''}`}>
          {['ABOUT', 'TRY', 'GLYPH', 'ARCHITECTURE'].map((item) => {
            const id = item.toLowerCase();
            const isActive = activeSection === id;
            return (
              <li key={item} className="nav-item">
                <a
                  href={`#${id}`}
                  onClick={(e) => {
                    e.preventDefault();
                    setIsMobileMenuOpen(false);
                    scrollToSection(id);
                  }}
                  className={`nav-link ${isActive ? 'active' : ''}`}
                >
                  <span className="nav-blob"></span>
                  <span style={{ position: 'relative', zIndex: 12 }}>{item}</span>
                </a>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Header Strip below Nav links at the top (disappears on scroll) */}
      <div className={`header-strip-container ${isScrolled ? 'scrolled-away' : ''}`}>
        <img src={header} alt="Curse You" className="header-strip-img" />
      </div>

      {/* 2. Hero Section */}
      <section className="section hero-section" id="hero">
        <img src={hero} alt="Curse You" className="hero-collage" />
        <button className="hero-try-btn" onClick={() => scrollToSection('try')}>TRY THE DEMO</button>
      </section>

      {/* 3. ABOUT Section (Redesigned split card flow) */}
      <section className="section about-section" id="about">
        <div className="about-grid">
          
          <div className="about-premium-card">
            <h2 className="about-headline">ABOUT</h2>
            <div className="about-desc">
              CurseYou is an interactive digital art installation exploring the intersections 
              of geography, language, and typography. By analyzing the organic, meandering contours of the Amazon's 
              river channels, we have created a dynamic, living script. Our custom layout engine maps 
              the natural bends, oxbows, and branches of satellite river paths onto standard typographic glyphs. 
              The result is a flowing, continuous river network that spells out your name—a dialogue 
              between digital layout algorithms and the earth's natural topography.
            </div>
          </div>

          <div className="about-right-flow">
            <div className="about-node-box">
              <div className="about-node-circle">01</div>
              <div className="about-node-text">
                <h4>Satellite Contours</h4>
                <p>Curating real river paths extracted from high-resolution satellite imagery.</p>
              </div>
            </div>
            
            <div className="about-node-box">
              <div className="about-node-circle">02</div>
              <div className="about-node-text">
                <h4>Fluid Typography</h4>
                <p>Translating standard English letters into natural geographic meanders.</p>
              </div>
            </div>

            <div className="about-node-box">
              <div className="about-node-circle">03</div>
              <div className="about-node-text">
                <h4>Stitching Optimizer</h4>
                <p>Finding candidate overlapping points dynamically to stitch letters seamlessly.</p>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* 4. TRY Section */}
      <section className="section try-section" id="try">
        <div className="try-container">
          {isLoading ? (
            <div className="try-loading-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
              <div className="try-spinner" style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: '5px solid rgba(163, 217, 0, 0.2)',
                borderTop: '5px solid var(--lime-green)',
                animation: 'spin 1s linear infinite'
              }}></div>
              <div style={{ fontFamily: 'var(--font-nav)', color: 'var(--lime-green)', fontSize: '1.5rem', letterSpacing: '0.05em' }}>GENERATING RIVER...Backend is on Render so it may take a while</div>
            </div>
          ) : apiError ? (
            <div style={{ fontFamily: 'var(--font-nav)', color: '#ff6b6b', fontSize: '1.5rem', textAlign: 'center', padding: '2rem' }}>
              ERROR: {apiError}
            </div>
          ) : generatedImage ? (
            <img 
              src={generatedImage} 
              alt={tryText} 
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
                borderRadius: '40px',
                padding: '10px'
              }} 
            />
          ) : (
            <div className="try-output-text">
              {tryText || 'ENTER A NAME'}
            </div>
          )}
        </div>

        <div className="try-controls">
          <div className="try-input-group">
            <span className="try-label">ENTER A NAME :</span>
            <input
              type="text"
              className="try-input"
              value={tryText}
              onChange={(e) => setTryText(e.target.value.toUpperCase())}
              placeholder={placeholderText}
              maxLength={20}
            />
          </div>

          <div className="try-buttons">
            {/* Left Circular Button: Download Generated Image */}
            <button
              onClick={handleDownloadImage}
              className="circle-btn"
              title="Download Image"
              aria-label="Download Image"
              disabled={!generatedImage}
              style={{ opacity: generatedImage ? 1 : 0.4, cursor: generatedImage ? 'pointer' : 'not-allowed' }}
            >
              ⤓
            </button>
            {/* Right Circular Button: Reset (Picks new random name) */}
            <button
              onClick={handleResetName}
              className="circle-btn"
              title="Reset Name"
              aria-label="Reset Name"
            >
              ↺
            </button>
          </div>
        </div>
      </section>

      {/* 5. GLYPH Section */}
      <section className="section glyph-section" id="glyph">
        <div className="glyph-layout">
          
          {/* Left: Interactive Vector Display Area */}
          <div className="glyph-display-area">
            <div className="glyph-guide-lines">
              <div className="guide-line"></div>
              <div className="guide-line"></div>
              <div className="guide-line"></div>
            </div>

            <svg viewBox="0 0 400 500" className="glyph-svg-canvas">
              {activeKey && GLYPH_PATHS[activeKey] && (
                <path
                  key={activeKey}
                  d={GLYPH_PATHS[activeKey]}
                  className="glyph-river-path"
                />
              )}
            </svg>
          </div>

          {/* Right: Custom Hexagonal Keyboard */}
          <div className="glyph-keyboard-container">
            {KEYBOARD_ROWS.map((row, rIdx) => (
              <div key={rIdx} className={`hex-row ${row.staggered ? 'staggered' : ''}`}>
                {row.keys.map((key) => {
                  const isActive = activeKey === key;
                  return (
                    <div
                      key={key}
                      onClick={() => handleHexKeyClick(key)}
                      className={`hex-key ${isActive ? 'active' : ''}`}
                    >
                      <span className="hex-key-label">{key}</span>
                    </div>
                  );
                })}
              </div>
            ))}
          </div>

          {/* Bottom center: Download controls (replacing text input) */}
          <div className="glyph-input-wrapper" style={{ display: 'flex', gap: '2rem', justifyContent: 'center', width: '100%', gridColumn: 'span 2' }}>
            <button
              onClick={handleDownloadTxt}
              style={{
                backgroundColor: 'var(--forest-green)',
                border: '3px solid transparent',
                borderRadius: '30px',
                height: '60px',
                padding: '0 2rem',
                fontFamily: 'var(--font-nav)',
                fontSize: '1.25rem',
                color: 'var(--lime-green)',
                cursor: 'pointer',
                outline: 'none',
                boxShadow: '0 10px 30px rgba(0, 0, 0, 0.4)',
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = 'var(--lime-green)';
                e.target.style.color = 'var(--forest-green)';
                e.target.style.transform = 'scale(1.05)';
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = 'var(--forest-green)';
                e.target.style.color = 'var(--lime-green)';
                e.target.style.transform = 'scale(1)';
              }}
            >
              Download Text (.txt)
            </button>
            <button
              onClick={handleDownloadLetterImage}
              style={{
                backgroundColor: 'var(--forest-green)',
                border: '3px solid transparent',
                borderRadius: '30px',
                height: '60px',
                padding: '0 2rem',
                fontFamily: 'var(--font-nav)',
                fontSize: '1.25rem',
                color: 'var(--lime-green)',
                cursor: 'pointer',
                outline: 'none',
                boxShadow: '0 10px 30px rgba(0, 0, 0, 0.4)',
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = 'var(--lime-green)';
                e.target.style.color = 'var(--forest-green)';
                e.target.style.transform = 'scale(1.05)';
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = 'var(--forest-green)';
                e.target.style.color = 'var(--lime-green)';
                e.target.style.transform = 'scale(1)';
              }}
            >
              Download Letter (.svg)
            </button>
          </div>

        </div>
      </section>

      {/* 6. ARCHITECTURE Section (Redesigned 6-Step Technical Vertical Timeline) */}
      <section className="section architecture-section" id="architecture">
        <h2 style={{ fontFamily: 'var(--font-nav)', fontSize: '3rem', color: 'var(--lime-green)', letterSpacing: '0.05em', marginBottom: '1rem' }}>ARCHITECTURE</h2>
        <p style={{ maxWidth: '850px', color: 'var(--light-olive)', fontSize: '1.2rem', lineHeight: '1.6', marginBottom: '2.5rem' }}>
          CurseYou relies on an automated layout and stitching pipeline running in our Python backend. 
          By connecting satellite imagery vectors with graph optimization algorithms, we compose smooth river lines.
        </p>

        <div className="timeline-container">
          <div className="timeline-bar"></div>

          {/* Step 1 */}
          <div className="timeline-item">
            <div className="timeline-dot"></div>
            <div className="timeline-card">
              <h3><span>01</span> Feature Vector Mapping</h3>
              <p>
                We extract high-resolution centerline splines from Google Earth and NASA Landsat imagery. 
                Each river curve is cataloged as a parametric function:
              </p>
              <span className="math-expr">S(t) = &Sigma; B_i(t) &middot; P_i</span>
              <p>mapping raw geographic water paths to discrete vector graphics.</p>
            </div>
            <div className="timeline-media-box">
              <span className="media-icon">📷</span>
              <span className="media-label">[ Satellite Snippet Image ]</span>
            </div>
          </div>

          {/* Step 2 */}
          <div className="timeline-item">
            <div className="timeline-dot"></div>
            <div className="timeline-card">
              <h3><span>02</span> Spline Signature Indexing</h3>
              <p>
                Each river letter segment is indexed in our database. We measure entrance/exit flow angles 
                (&theta;<sub>in</sub>, &theta;<sub>out</sub>) and channel widths (W<sub>in</sub>, W<sub>out</sub>) 
                to guarantee seamless physical properties between adjoining meander nodes.
              </p>
            </div>
            <div className="timeline-media-box">
              <span className="media-icon">🏷️</span>
              <span className="media-label">[ Letter Signature Index ]</span>
            </div>
          </div>

          {/* Step 3 */}
          <div className="timeline-item">
            <div className="timeline-dot"></div>
            <div className="timeline-card">
              <h3><span>03</span> Beam Search Optimization</h3>
              <p>
                A search algorithm matches adjoining letter candidates. It evaluates combinations by 
                minimizing a boundary cost mismatch function:
              </p>
              <span className="math-expr">E_joint = w_&theta;(&Delta;&theta;)^2 + w_w(&Delta;W)^2</span>
              <p>ensuring natural continuation without bottlenecks or unrealistic bends.</p>
            </div>
            <div className="timeline-media-box">
              <span className="media-icon">📈</span>
              <span className="media-label">[ Graph Path Node Mesh ]</span>
            </div>
          </div>

          {/* Step 4 */}
          <div className="timeline-item">
            <div className="timeline-dot"></div>
            <div className="timeline-card">
              <h3><span>04</span> Rigid Body Alignment</h3>
              <p>
                To stitch the sequence, individual segments are translated and rotated into place. 
                The layout engine computes a 2D affine transformation:
              </p>
              <span className="math-expr">P_new = R(&Delta;&theta;) &middot; P + T</span>
              <p>mapping the exit node of letter k to the entrance node of k+1.</p>
            </div>
            <div className="timeline-media-box">
              <span className="media-icon">🔗</span>
              <span className="media-label">[ Stitched River Channel Layout ]</span>
            </div>
          </div>

          {/* Step 5 */}
          <div className="timeline-item">
            <div className="timeline-dot"></div>
            <div className="timeline-card">
              <h3><span>05</span> Junction Alpha Blending</h3>
              <p>
                Overlap zones are resolved using dynamic feathering masks and linear transparency blending:
              </p>
              <span className="math-expr">C_blend = &alpha; &middot; C_A + (1 - &alpha;) &middot; C_B</span>
              <p>This merges satellite banks, preventing sudden seams or color shifts at joint lines.</p>
            </div>
            <div className="timeline-media-box">
              <span className="media-icon">🎨</span>
              <span className="media-label">[ Final Composite Mask Render ]</span>
            </div>
          </div>

          {/* Step 6 */}
          <div className="timeline-item">
            <div className="timeline-dot"></div>
            <div className="timeline-card">
              <h3><span>06</span> Matte Composition</h3>
              <p>
                The finalized river ribbon is composited over forest textures. Post-processing steps 
                apply local color adjustments and super-resolution upscaling to export a printable image.
              </p>
            </div>
            <div className="timeline-media-box">
              <span className="media-icon">🖥️</span>
              <span className="media-label">[ Final Output Image ]</span>
            </div>
          </div>

        </div>
      </section>

      {/* 7. Footer Section */}
      <section className="section footer-section" id="footer">
        <div className="footer-graphic-container">
          <img src={footer} alt="Thank You" className="footer-graphic footer-graphic-container-img" />
        </div>
        <div className="footer-content">
          <div className="footer-brand">curse you</div>
          
          <div className="footer-split-grid">
            {/* Left Column: Work in progress */}
            <div className="footer-col-left">
              <h4 className="footer-heading">Project Status</h4>
              <p className="footer-desc">
                CurseYou is currently a <strong>Work in Progress</strong>. I'm actively building out features, 
                and development on the Glyph vector engine is currently ongoing. 
                If you have ideas or would like to help contribute to this river project:
              </p>
              <a href="https://github.com/ShantanuGV/CuresYou" target="_blank" rel="noopener noreferrer" className="footer-github-link">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" style={{ marginRight: '0.6rem' }}>
                  <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
                </svg>
                Contribute on GitHub
              </a>
            </div>

            {/* Right Column: Inspirations */}
            <div>
              <h4 className="footer-heading">Inspirations</h4>
              <ul className="inspiration-list">
                <li className="inspiration-item">
                  <a href="https://newglyph.com/typeface/amazonia/" target="_blank" rel="noopener noreferrer">Newglyph Amazonia Typeface</a>
                </li>
                <li className="inspiration-item">
                  <a href="https://igaratipo.visiteamazonia.com.br/" target="_blank" rel="noopener noreferrer">Igara Tipo (Amazonia Typographic Meander)</a>
                </li>
                <li className="inspiration-item">
                  <a href="https://science.nasa.gov/specials/your-name-in-landsat/" target="_blank" rel="noopener noreferrer">NASA - Your Name in Landsat</a>
                </li>
              </ul>
              <p style={{ marginTop: '1.5rem', fontSize: '0.85rem', color: 'var(--light-olive)', opacity: 0.8 }}>
                Imagery content matches Google Maps and Google Earth satellite contours.
              </p>
            </div>
          </div>

          <ul className="footer-links">
            <li><a href="#hero" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="footer-link">Home</a></li>
            <li><a href="#about" onClick={(e) => { e.preventDefault(); scrollToSection('about'); }} className="footer-link">About</a></li>
            <li><a href="#try" onClick={(e) => { e.preventDefault(); scrollToSection('try'); }} className="footer-link">Try</a></li>
            <li><a href="#glyph" onClick={(e) => { e.preventDefault(); scrollToSection('glyph'); }} className="footer-link">Glyph</a></li>
            <li><a href="#architecture" onClick={(e) => { e.preventDefault(); scrollToSection('architecture'); }} className="footer-link">Architecture</a></li>
          </ul>

          <div className="footer-copy" style={{ color: 'rgba(203, 214, 181, 0.5)', fontSize: '1.05rem', marginTop: '1.5rem' }}>
            Created by <a href="https://shantanugv.vercel.app/" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--lime-green)', textDecoration: 'underline', fontWeight: 'bold' }}>Shantanu Gopal Vispute</a>. &copy; {new Date().getFullYear()} CurseYou.
          </div>
        </div>
      </section>
    </>
  );
}

export default App;
export default App;
