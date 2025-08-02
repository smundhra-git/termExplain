class Termexplain < Formula
    desc "AI-powered CLI error explainer using Gemini"
    homepage "https://github.com/smundhra-git/termExplain"
    url "https://github.com/smundhra-git/termExplain/archive/refs/tags/v1.0.0.tar.gz"
    sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5" 
    license "MIT"
    head "https://github.com/smundhra-git/termExplain.git", branch: "main"
  
    depends_on "python@3.8"
  
    def install
      # Install Python dependencies
      system "python3", "-m", "pip", "install", *std_pip_args, "."
      
      # Create the explain script
      bin.install "explain.sh" => "explain"
      
      # Make the main script executable
      chmod 0755, "main.py"
      bin.install "main.py" => "termexplain"
    end
  
    test do
      # Test that the command works
      system "#{bin}/termexplain", "--version"
    end
  
    def caveats
      <<~EOS
        termExplain requires a Gemini API key to function.
        
        Set your API key:
          export GEMINI_API_KEY="your-api-key-here"
        
        Or add to your shell profile (~/.zshrc or ~/.bashrc):
          echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
        
        Get your API key from: https://aistudio.google.com/
        
        Usage:
          explain "your error message here"
          explain --file your_script.py
      EOS
    end
  end