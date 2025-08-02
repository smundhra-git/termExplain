class Termexplain < Formula
    include Language::Python::Virtualenv
  
    desc "AI-powered CLI error explainer using Gemini"
    homepage "https://github.com/smundhra-git/termExplain"
    url "https://github.com/smundhra-git/termExplain/archive/refs/tags/v1.0.0.tar.gz"
    sha256 "da7de1993cf7fa3b2f0cd26532fd93779fd5f0b344a75fa3d51e296ccfa9474f"
    license "MIT"
    head "https://github.com/smundhra-git/termExplain.git", branch: "main"
  
    depends_on "python@3.11"
  
    def install
      virtualenv_install_with_resources
  
      # Install CLI wrapper
      bin.install "explain.sh" => "explain"
  
      # Fix the script path inside the wrapper
      inreplace bin/"explain", "$SCRIPT_DIR/main.py", libexec/"bin/termexplain"
    end
  
    resource "google-generativeai" do
      url "https://files.pythonhosted.org/packages/source/g/google-generativeai/google_generativeai-0.3.0-py3-none-any.whl"
      sha256 "7c28ca71f32d59396580f5a4ccfb0d431f8b1000fbba982e632d06ea6d121770"
    end
    
    resource "click" do
      url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.0-py3-none-any.whl"
      sha256 "19a4baa64da924c5e0cd889aba8e947f280309f1a2ce0947a3e3a7bcb7cc72d6"
    end
    
    resource "rich" do
      url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.0.0-py3-none-any.whl"
      sha256 "12b1d77ee7edf251b741531323f0d990f5f570a4e7c054d0bfb59fb7981ad977"
    end
    
    resource "colorama" do
      url "https://files.pythonhosted.org/packages/source/c/colorama/colorama-0.4.6-py2.py3-none-any.whl"
      sha256 "4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6"
    end
    
    resource "python-dotenv" do
      url "https://files.pythonhosted.org/packages/source/p/python-dotenv/python_dotenv-1.0.0-py3-none-any.whl"
      sha256 "f5971a9226b701070a4bf2c38c89e5a3f0d64de8debda981d1db98583009122a"
    end
    
    resource "requests" do
      url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.31.0-py3-none-any.whl"
      sha256 "58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003f"
    end
    
  
    test do
      system "#{bin}/explain", "echo 'Test error'"
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
      EOS
    end
  end
  