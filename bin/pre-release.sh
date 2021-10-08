pushd docs
make html
make markdown
cp -r build/html/ html
cp -r build/markdown/ markdown
popd
