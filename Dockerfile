FROM gcc:15.1.0-bookworm AS nanobench-build
RUN <<EOF 
git clone --depth 1 --branch v4.3.11 https://github.com/martinus/nanobench.git /nanobench
mkdir /build
mv /nanobench/src/include/nanobench.h /build
EOF
WORKDIR /build
COPY <<EOF nanobench.cpp
#define ANKERL_NANOBENCH_IMPLEMENT
#include "nanobench.h"
EOF
RUN g++ -O3 -c -o nanobench.o nanobench.cpp

FROM gcc:15.1.0-bookworm
COPY --from=nanobench-build /build/nanobench.o /build/nanobench.h /usr/src/
