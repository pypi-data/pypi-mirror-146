
#include <iostream>
#include <memory>
#include <vector>

#include "kompute/Kompute.hpp"

static
std::vector<uint32_t>
compileSource(
  const std::string& source)
{
    std::ofstream fileOut("tmp_kp_shader.comp");
	fileOut << source;
	fileOut.close();
    if (system(std::string("glslangValidator -V tmp_kp_shader.comp -o tmp_kp_shader.comp.spv").c_str()))
        throw std::runtime_error("Error running glslangValidator command");
    std::ifstream fileStream("tmp_kp_shader.comp.spv", std::ios::binary);
    std::vector<char> buffer;
    buffer.insert(buffer.begin(), std::istreambuf_iterator<char>(fileStream), {});
    return {(uint32_t*)buffer.data(), (uint32_t*)(buffer.data() + buffer.size())};
}

int main()
{
#if KOMPUTE_ENABLE_SPDLOG
    spdlog::set_level(
      static_cast<spdlog::level::level_enum>(SPDLOG_ACTIVE_LEVEL));
#endif

    kp::Manager mgr;

    auto tensorInA = mgr.tensor({ 2.0, 4.0, 6.0 });
    auto tensorInB = mgr.tensor({ 0.0, 1.0, 2.0 });
    auto tensorOut = mgr.tensor({ 0.0, 0.0, 0.0 });

    std::string shader(R"(
        // The version to use 
        #version 450

        // The execution structure
        layout (local_size_x = 1) in;

        // The buffers are provided via the tensors
        layout(binding = 0) buffer bufA { float a[]; };
        layout(binding = 1) buffer bufB { float b[]; };
        layout(binding = 2) buffer bufOut { float o[]; };

        void main() {
            uint index = gl_GlobalInvocationID.x;

            o[index] = a[index] * b[index];
        }
      )");

    std::vector<std::shared_ptr<kp::Tensor>> params = { tensorInA, tensorInB, tensorOut };

    std::shared_ptr<kp::Algorithm> algo = mgr.algorithm(params, compileSource(shader));

    mgr.sequence()
        ->record<kp::OpTensorSyncDevice>(params)
        ->record<kp::OpAlgoDispatch>(algo)
        ->record<kp::OpTensorSyncLocal>(params)
        ->eval();

    // prints "Output {  0  4  12  }"
    std::cout<< "Output: {  ";
    for (const float& elem : tensorOut->vector()) {
      std::cout << elem << "  ";
    }
    std::cout << "}" << std::endl;
}

