#!/bin/bash
# ══════════════════════════════════════════════
#  🐝 رفع لعبة الحروف إلى GitHub Pages
#  شغّل هذا الملف مرة واحدة فقط
# ══════════════════════════════════════════════

echo ""
echo "🐝 رفع لعبة الحروف إلى GitHub Pages"
echo "══════════════════════════════════════"
echo ""

# Check git
if ! command -v git &> /dev/null; then
  echo "❌ Git غير مثبت. حمّله من: https://git-scm.com"
  exit 1
fi

# Get GitHub username
read -p "👤 اسم مستخدم GitHub الخاص بك: " GITHUB_USER
if [ -z "$GITHUB_USER" ]; then
  echo "❌ اسم المستخدم فارغ"
  exit 1
fi

REPO_NAME="arabic-hex-game"
echo ""
echo "📁 سيتم إنشاء: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "🌐 الدومين سيكون: https://$GITHUB_USER.github.io/$REPO_NAME"
echo ""

# Init git
git init
git add .
git commit -m "🐝 Initial commit - Arabic Hex Game"
git branch -M main

echo ""
echo "📤 جارٍ الرفع إلى GitHub..."
echo ""
echo "⚠️  ستحتاج إلى:"
echo "   1. إنشاء مستودع جديد على GitHub باسم: $REPO_NAME"
echo "      https://github.com/new"
echo "   2. اجعله Public (عام)"
echo "   3. لا تضف README أو .gitignore"
echo ""
read -p "✅ بعد إنشاء المستودع، اضغط Enter للمتابعة..."

git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
git push -u origin main

echo ""
echo "══════════════════════════════════════"
echo "✅ تم الرفع بنجاح!"
echo ""
echo "📺 الآن فعّل GitHub Pages:"
echo "   1. افتح: https://github.com/$GITHUB_USER/$REPO_NAME/settings/pages"
echo "   2. Source: اختر 'GitHub Actions'"
echo "   3. انتظر دقيقة واحدة"
echo ""
echo "🎮 رابط اللعبة:"
echo "   https://$GITHUB_USER.github.io/$REPO_NAME"
echo ""
echo "🔔 رابط البازر:"
echo "   https://$GITHUB_USER.github.io/$REPO_NAME/buzzer"
echo "══════════════════════════════════════"
