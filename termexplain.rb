class Termexplain < Formula
  include Language::Python::Virtualenv

  desc "AI-powered CLI error explainer using Gemini"
  homepage "https://github.com/smundhra-git/termExplain"
  url "https://github.com/smundhra-git/termExplain/archive/refs/tags/v1.0.1.tar.gz"
  sha256 "5b83d2b5d6f238301981293d21d0a82d85e03e2947be43eb60165d95091ba0dd"
  license "MIT"
  head "https://github.com/smundhra-git/termExplain.git", branch: "main"

  depends_on "python@3.11"

  resource "google-generativeai" do
    url "https://files.pythonhosted.org/packages/f6/5d/e828bdc71950e4549163700ea9213edbae8eb76810a8a9b4ac7fb0b3a25b/google_generativeai-0.3.0-py3-none-any.whl"
    sha256 "f65de828bdc71950e4549163700ea9213edbae8eb76810a8a9b4ac7fb0b3a25b"
  end
  
  resource "click" do
    url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.0.tar.gz"
    sha256 "977c213473c7665d3aa092b41ff12063227751c41d7b17165013e10069cc5cd2"
  end
  
  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.0.0.tar.gz"
    sha256 "3aa9eba7219b8c575c6494446a59f702552efe1aa261e7eeb95548fa586e1950"
  end
  
  resource "colorama" do
    url "https://files.pythonhosted.org/packages/source/c/colorama/colorama-0.4.6.tar.gz"
    sha256 "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
  end
  
  resource "python-dotenv" do
    url "https://files.pythonhosted.org/packages/source/p/python-dotenv/python-dotenv-1.0.0.tar.gz"
    sha256 "a8df96034aae6d2d50a4ebe8216326c61c3eb64836776504fcca410e5937a3ba"
  end
  
  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.31.0.tar.gz"
    sha256 "942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
  end
  
  def install
    venv = virtualenv_create(libexec, "python3.11")
    venv.pip_install resources
    venv.pip_install_and_link buildpath
  end

  test do
    assert_match "error", shell_output("#{bin}/explain 'ModuleNotFoundError'", 1)
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
        explain --file script.py
        explain --version
    EOS
  end
end
