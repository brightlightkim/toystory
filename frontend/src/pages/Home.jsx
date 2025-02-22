import React from 'react';
import { motion } from 'framer-motion';
import { Brain, MessageCircle, BarChart2, Globe, Heart } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  const features = [
    {
      icon: <MessageCircle className="h-6 w-6 text-indigo-600" />,
      title: 'AI-Powered Conversations',
      description: 'Engage in natural conversations with our advanced AI counselor.',
    },
    {
      icon: <BarChart2 className="h-6 w-6 text-indigo-600" />,
      title: 'Emotion Analysis',
      description: 'Track your emotional well-being with real-time analysis.',
    },
    {
      icon: <Globe className="h-6 w-6 text-indigo-600" />,
      title: 'Multilingual Support',
      description: 'Get counseling in your preferred language.',
    },
    {
      icon: <Heart className="h-6 w-6 text-indigo-600" />,
      title: 'Personalized Care',
      description: 'Receive tailored advice based on your unique needs.',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span className="block">Your AI Companion for</span>
                <span className="block text-indigo-600">Mental Well-being</span>
              </h1>
              <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
                Experience the future of counseling with our AI-powered platform. Get support anytime, anywhere.
              </p>
            </motion.div>
            <div className="mt-10">
              <Link
                to="/counseling"
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Start Counseling Now
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900">Why Choose AI Counsel?</h2>
            <p className="mt-4 text-lg text-gray-500">
              Our platform combines cutting-edge AI technology with proven counseling methods.
            </p>
          </div>

          <div className="mt-20">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="relative p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
                >
                  <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-3 rounded-full shadow-lg">
                    {feature.icon}
                  </div>
                  <h3 className="mt-8 text-lg font-medium text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-base text-gray-500">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-indigo-700">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            <span className="block">Ready to get started?</span>
            <span className="block text-indigo-200">Begin your journey to better mental health today.</span>
          </h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
            <div className="inline-flex rounded-md shadow">
              <Link
                to="/counseling"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
              >
                Start Free Session
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;