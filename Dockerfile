FROM gcc:15.1.0-bookworm AS gbench-build
RUN apt update && apt install -y cmake
RUN git clone --depth 1 --branch v1.9.4 https://github.com/google/benchmark.git /benchmark
WORKDIR /benchmark
RUN <<EOF
cmake -E make_directory "build" &&\
cmake \
    -DBENCHMARK_ENABLE_GTEST_TESTS=OFF \
    -DBENCHMARK_DOWNLOAD_DEPENDENCIES=on \
    -DCMAKE_BUILD_TYPE=Release \
    -S . -B "build" &&\
cmake --build "build" --parallel --config Release
EOF

FROM gcc:15.1.0-bookworm
RUN mkdir -p /benchmark/lib
COPY --from=gbench-build /benchmark/include /benchmark/
COPY --from=gbench-build /benchmark/build/src/libbenchmark.a /benchmark/lib/
